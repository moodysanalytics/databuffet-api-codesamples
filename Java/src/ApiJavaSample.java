import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.util.concurrent.TimeUnit;
import java.util.stream.Stream;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

import com.google.gson.Gson;


public class ApiJavaSample {

	private static String UriEndpoint = "https://api.economy.com/data/v1/";
    private static String AccessKeyHeader = "AccessKeyId";
    private static String SignatureHeader = "Signature";
    private static String TimeStampHeader = "TimeStamp";
    private static String AccessKey = ""; //Your Access Key
    private static String EncryptionKey = ""; //Your Encryption Key

	
	// This Main method calls on subsequent methods to perform the following tasks
	// Get list of baskets, post an order to a basket, check the order status and retreive the contents of the ordered basket once completed
	public static void main(String[] args) throws Exception
	{
		
		String DeskTopLocation = System.getProperty("user.home") + "/Desktop".toString(); //All basket files are currently saved to the Desktop       
        String BasketId = ""; //BasketId you want to run
        String FileName = ""; //Name of File to be written once basket contents are retrieved		
		
		
		GetBaskets(AccessKey, EncryptionKey); // Calls the GetBaskets method to return list of baskets & basket metadata
		
		TimeUnit.SECONDS.sleep(1);

        if(BasketId == ""){
            
            System.out.println("Check the program output and (Ctrl + F) the name of your basekt. Then, replace the BasketId variable with your BasketId");

        } else{
            Gson gson = new Gson();
        String postResult = PostOrders(AccessKey, EncryptionKey,BasketId); // Calls the PostOrders method to POST an order to a basket (specified by BasketId)
        PostOrders postOrders = gson.fromJson(postResult, PostOrders.class);
        
        System.out.println(postOrders.orderId); // returns orderId from PostOrders method. 
        
        PostOrders orderStatus;
        boolean orderCompleted = false;
        while(!orderCompleted) // orderId is used to in loop to check if dataFinished attribute of order is not Null. When not Null, loop is exited. 
        {
            TimeUnit.SECONDS.sleep(1);
            
            String getOrdersResult = GetOrderStatus(AccessKey, EncryptionKey, postOrders.orderId);
            orderStatus = gson.fromJson(getOrdersResult, PostOrders.class);
            
            if(orderStatus.dateFinished != null) 
            {
                orderCompleted = true;
            }
        }
        
        TimeUnit.SECONDS.sleep(1);
        
        InputStream orderStream = GetOrderStream(AccessKey, EncryptionKey, BasketId); // Calls GetOrderSteam method using BasketId to return ordered basket's contents
        
        File targetFile = new File(DeskTopLocation + "\\" + FileName); 
    
        java.nio.file.Files.copy(
                  orderStream, 
                  targetFile.toPath(), 
                  StandardCopyOption.REPLACE_EXISTING); // writes basket's content to file (specified by FileName)
        
        }

	} // This is the end of the Main method. Following code represents the inidividual methods called in Main method.  
	
	
	    // GetBaskets Method will:
		// 		Generate new timeStamp & signature
		//		Make GET call to endpoint to retrieve basket list & basket metadata	
		// 		Http call response as json object 
	public static void GetBaskets(String accessKey, String encryptionKey) throws Exception
    {
		String timeStamp = ZonedDateTime.now(ZoneOffset.UTC).toString();
		String signature = CreateHMACSignature(accessKey, encryptionKey, timeStamp);

        URL url = new URL(UriEndpoint + "baskets");
        
        HttpURLConnection httpConnection = (HttpURLConnection) url.openConnection();
        
        httpConnection.setRequestMethod("GET");
        httpConnection.setRequestProperty(AccessKeyHeader, accessKey);
        httpConnection.setRequestProperty(TimeStampHeader, timeStamp);
        httpConnection.setRequestProperty(SignatureHeader, signature);
        
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
		// 		Generate new timestamp and signature 
		// 		Make POST call to endpoint to order a basket (using BasketId)
        // 		Http call response is returned as JSON

	public static String PostOrders(String accessKey, String encryptionKey, String BasketId) throws Exception
    {
		String timeStamp = ZonedDateTime.now(ZoneOffset.UTC).toString();
		String signature = CreateHMACSignature(accessKey, encryptionKey, timeStamp);

        URL url = new URL(UriEndpoint + "orders" + "?id=" + BasketId + "&type=baskets&action=run"); // endpoint to call to 
        
        HttpURLConnection httpConnection = (HttpURLConnection) url.openConnection();
        
        httpConnection.setRequestMethod("POST");
        httpConnection.setRequestProperty(AccessKeyHeader, accessKey);
        httpConnection.setRequestProperty(TimeStampHeader, timeStamp);
        httpConnection.setRequestProperty(SignatureHeader, signature);
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
		// 		Generate new timestamp & signature
		//		Make GET call to endpoint to retrieve order metadata 
		// 		http call response is returned as JSON 
        // 		
	public static String GetOrderStatus(String accessKey, String encryptionKey, String orderID) throws Exception
    {
		String timeStamp = ZonedDateTime.now(ZoneOffset.UTC).toString();
		String signature = CreateHMACSignature(accessKey, encryptionKey, timeStamp);

        URL url = new URL(UriEndpoint + "orders/" + orderID); // endpoint to call to 
        
        HttpURLConnection httpConnection = (HttpURLConnection) url.openConnection();
        
        httpConnection.setRequestMethod("GET");
        httpConnection.setRequestProperty(AccessKeyHeader, accessKey);
        httpConnection.setRequestProperty(TimeStampHeader, timeStamp);
        httpConnection.setRequestProperty(SignatureHeader, signature);
        
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
		
		//CreateHMACSignature Method will: 
		//		Create & return signature 
        // 		This method is used in all preceeding methods except main method  
	public static String CreateHMACSignature(String accessKey, String encryptionKey, String timeStamp)  throws Exception
	{
       byte[] hmacData = null;
       String signature = "",
               combinedKey = accessKey + timeStamp;
       //Create a new key from the encryption key passed in.
       SecretKeySpec secretKey = new SecretKeySpec(encryptionKey.getBytes("UTF-8"), "HmacSHA256");

       //Create a new hmac sha-256 mac instance
       Mac mac = Mac.getInstance("HmacSHA256");
       //Initializes this Mac instance with the secret key
       mac.init(secretKey);
       //Computes the digest of this MAC on the bytes specified
       hmacData = mac.doFinal(combinedKey.getBytes("UTF-8"));

       //Take one byte at a time from the byte array and convert them to Hex, add them to the signature string.
       for(byte b : hmacData){
           signature += String.format("%02X", b);
       }
       return signature;
   }
	
	
	
	    // GetOrderStream method will : 
		// 		Generate new timeStamp & signature
		// 		Make GET call to endpoint to contents of ordered basket (using BasketId)
        // 		Assigns response to stream
	public static InputStream GetOrderStream(String accessKey, String encryptionKey, String BasketId) throws Exception
    {
		String timeStamp = ZonedDateTime.now(ZoneOffset.UTC).toString();
		String signature = CreateHMACSignature(accessKey, encryptionKey, timeStamp);

        URL url = new URL(UriEndpoint + "orders"+ "?id=" + BasketId + "&type=baskets"); // endpoint to call to 
        
        HttpURLConnection httpConnection = (HttpURLConnection) url.openConnection();
        
        httpConnection.setRequestMethod("GET");
        httpConnection.setRequestProperty(AccessKeyHeader, accessKey);
        httpConnection.setRequestProperty(TimeStampHeader, timeStamp);
        httpConnection.setRequestProperty(SignatureHeader, signature);
        
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
