import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.File;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.StandardCopyOption;
import java.util.concurrent.TimeUnit;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;


public class ApiJavaSample {

	private static String UriEndpoint = "https://api.economy.com/data/v1/";
    private static String AccessKey = ""; //Your Access Key
    private static String EncryptionKey = ""; //Your Encryption Key

	
	// This Main method calls on subsequent methods to perform the following tasks
	// Get list of baskets, post an order to a basket, check the order status and retreive the contents of the ordered basket once completed
	public static void main(String[] args) throws Exception
	{
		
		String DeskTopLocation = System.getProperty("user.home") + "/Desktop".toString(); //All basket files are currently saved to the Desktop
        String BasketId = ""; //BasketId you want to run
        String FileName = ""; //Name of File to be written once basket contents are retrieved

		// Fetch an OAuth 2.0 bearer token once and reuse it for every request below.
		// Tokens are valid for one hour.
		String token = getOAuthToken(AccessKey, EncryptionKey);

		GetBaskets(token); // Calls the GetBaskets method to return list of baskets & basket metadata

		TimeUnit.SECONDS.sleep(1);

        if(BasketId == ""){

            System.out.println("Check the program output and (Ctrl + F) the name of your basekt. Then, replace the BasketId variable with your BasketId");

        } else{
            Gson gson = new Gson();
        String postResult = PostOrders(token, BasketId); // Calls the PostOrders method to POST an order to a basket (specified by BasketId)
        PostOrders postOrders = gson.fromJson(postResult, PostOrders.class);

        System.out.println(postOrders.orderId); // returns orderId from PostOrders method.

        PostOrders orderStatus;
        boolean orderCompleted = false;
        while(!orderCompleted) // orderId is used to in loop to check if dataFinished attribute of order is not Null. When not Null, loop is exited.
        {
            TimeUnit.SECONDS.sleep(1);

            String getOrdersResult = GetOrderStatus(token, postOrders.orderId);
            orderStatus = gson.fromJson(getOrdersResult, PostOrders.class);

            if(orderStatus.dateFinished != null)
            {
                orderCompleted = true;
            }
        }

        TimeUnit.SECONDS.sleep(1);

        InputStream orderStream = GetOrderStream(token, BasketId); // Calls GetOrderSteam method using BasketId to return ordered basket's contents
        
        File targetFile = new File(DeskTopLocation + "\\" + FileName); 
    
        java.nio.file.Files.copy(
                  orderStream, 
                  targetFile.toPath(), 
                  StandardCopyOption.REPLACE_EXISTING); // writes basket's content to file (specified by FileName)
        
        }

	} // This is the end of the Main method. Following code represents the inidividual methods called in Main method.  
	
	
	    // GetBaskets Method will:
		//		Make GET call to endpoint to retrieve basket list & basket metadata
		// 		Http call response as json object
	public static void GetBaskets(String token) throws Exception
    {
        URL url = new URL(UriEndpoint + "baskets");

        HttpURLConnection httpConnection = (HttpURLConnection) url.openConnection();

        httpConnection.setRequestMethod("GET");
        httpConnection.setRequestProperty("Authorization", "Bearer " + token);

        try 
        {
            //Create a buffer for reading off the http input stream.
            BufferedReader inputBuffet = new BufferedReader(new InputStreamReader(httpConnection.getInputStream()));

            String responseData = "";

            String inputLine;

            //Read one line at a time to from the buffet and add it to the response string.
            while ((inputLine = inputBuffet.readLine()) != null) 
            {
                responseData += inputLine;
            }
            inputBuffet.close();

            //Print response data from API.
            System.out.println(responseData.toString());
            
        }
        catch(Exception ex)
        {
            System.out.println(ex.toString());
        }
        
    }
	    // PostOrders method  will :
		// 		Make POST call to endpoint to order a basket (using BasketId)
        // 		Http call response is returned as JSON

	public static String PostOrders(String token, String BasketId) throws Exception
    {
        URL url = new URL(UriEndpoint + "orders" + "?id=" + BasketId + "&type=baskets&action=run"); // endpoint to call to

        HttpURLConnection httpConnection = (HttpURLConnection) url.openConnection();

        httpConnection.setRequestMethod("POST");
        httpConnection.setRequestProperty("Authorization", "Bearer " + token);
        httpConnection.setRequestProperty("Content-Length", "0");
        httpConnection.setDoOutput(true);
        
        byte[] data = {};
        
        DataOutputStream wr = new DataOutputStream( httpConnection.getOutputStream());
        
        wr.write( data );
        wr.flush();	
        
        
        try 
        {
            //Create a buffer for reading off the http input stream.
            BufferedReader inputBuffet = new BufferedReader(new InputStreamReader(httpConnection.getInputStream()));

            String responseData = "";

            String inputLine;

            //Read one line at a time to from the buffet and add it to the response string.
            while ((inputLine = inputBuffet.readLine()) != null) 
            {
                responseData += inputLine;
            }
            inputBuffet.close();

            //Print response data from API.
            System.out.println(responseData.toString());
            
            return responseData.toString();
            
        }
        catch(Exception ex)
        {
            System.out.println(ex.toString());
            
            return ex.toString();
        }

    }
	    // GetOrderStatus method  will:
		//		Make GET call to endpoint to retrieve order metadata
		// 		http call response is returned as JSON
        //
	public static String GetOrderStatus(String token, String orderID) throws Exception
    {
        URL url = new URL(UriEndpoint + "orders/" + orderID); // endpoint to call to

        HttpURLConnection httpConnection = (HttpURLConnection) url.openConnection();

        httpConnection.setRequestMethod("GET");
        httpConnection.setRequestProperty("Authorization", "Bearer " + token);

        try 
        {
            //Create a buffer for reading off the http input stream.
            BufferedReader inputBuffet = new BufferedReader(new InputStreamReader(httpConnection.getInputStream()));

            String responseData = "";

            String inputLine;

            //Read one line at a time to from the buffet and add it to the response string.
            while ((inputLine = inputBuffet.readLine()) != null) 
            {
                responseData += inputLine;
            }
            inputBuffet.close();

            //Print response data from API.
            System.out.println(responseData.toString());
            
            return responseData.toString();
            
        }
        catch(Exception ex)
        {
            System.out.println(ex.toString());
            
            return ex.toString();
        }
        
    }
		
		// getOAuthToken Method will:
		//		POST the access key and encryption key to the OAuth 2.0 token endpoint
		//		Return the bearer access token, which is valid for one hour
        // 		The returned token is passed to every other method as the "token" argument.
	public static String getOAuthToken(String accessKey, String encryptionKey)  throws Exception
	{
        URL url = new URL(UriEndpoint + "oauth2/token");

        HttpURLConnection httpConnection = (HttpURLConnection) url.openConnection();

        httpConnection.setRequestMethod("POST");
        httpConnection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
        httpConnection.setDoOutput(true);

        String body = "client_id=" + accessKey +
                      "&client_secret=" + encryptionKey +
                      "&grant_type=client_credentials";

        DataOutputStream wr = new DataOutputStream(httpConnection.getOutputStream());
        wr.writeBytes(body);
        wr.flush();
        wr.close();

        //Create a buffer for reading off the http input stream.
        BufferedReader inputBuffet = new BufferedReader(new InputStreamReader(httpConnection.getInputStream()));

        String responseData = "";
        String inputLine;
        while ((inputLine = inputBuffet.readLine()) != null)
        {
            responseData += inputLine;
        }
        inputBuffet.close();

        //Parse the JSON response and return the access token.
        //Note: with gson 2.2.2, fromJson(..., JsonObject.class) returns an empty
        //object, so use JsonParser to read the token out of the response.
        JsonObject tokenResponse = new JsonParser().parse(responseData).getAsJsonObject();
        return tokenResponse.get("access_token").getAsString();
   }



	    // GetOrderStream method will :
		// 		Make GET call to endpoint to contents of ordered basket (using BasketId)
        // 		Assigns response to stream
	public static InputStream GetOrderStream(String token, String BasketId) throws Exception
    {
        URL url = new URL(UriEndpoint + "orders"+ "?id=" + BasketId + "&type=baskets"); // endpoint to call to

        HttpURLConnection httpConnection = (HttpURLConnection) url.openConnection();

        httpConnection.setRequestMethod("GET");
        httpConnection.setRequestProperty("Authorization", "Bearer " + token);

        try 
        {
            //Create a buffer for reading off the http input stream.
            InputStream stream = httpConnection.getInputStream();
            
            return stream;
            
        }
        catch(Exception ex)
        {
            System.out.println(ex.toString());
            
            InputStream emptyStream = null;
            return emptyStream;
        }
        
    }

}
