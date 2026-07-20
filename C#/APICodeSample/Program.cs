using System;
using System.IO;
using System.Net;
using System.Text;
using Newtonsoft.Json;
// Newtonsoft.Json used for serializing & deserializing JSON objects

namespace APICodeSample
{
    class Program
    {
        private const string UriEndpoint = "https://api.economy.com/data/v1/";
        private const string AccessKey = ""; // Enter Your Access Key
        private const string EncryptionKey = ""; // Enter Your Encryption Key


        // This Main method calls on subsequent methods to perform the following tasks
        // Get list of baskets, post an order to a basket, check the order status and retreive the contents of the ordered basket once completed
        static void Main(string[] args)
        {
            string BasketId = ""; //BasketId of basket you want to run 
            string FileName = ""; // Enter Filename that basket contents will be written to
            string DesktopLocation = Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory); //All logs and basket files are currently saved to the Desktop

            // Apps targeting .NET Framework 4.5.2 default to TLS 1.0, which the API rejects.
            // Opt into TLS 1.2 before making any request.
            ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;

            // Fetch an OAuth 2.0 bearer token once and reuse it for every request below.
            // Tokens are valid for one hour.
            string token = GetOAuthToken(AccessKey, EncryptionKey);

            string singleSeries = GetSingleSeries(token, "ET.IUSA");
            var jsonSingleSeries = JsonConvert.DeserializeObject(singleSeries);
            File.WriteAllText(String.Format(@"{0}\SingleSeries.json", DesktopLocation), JsonConvert.SerializeObject(jsonSingleSeries, Formatting.Indented));

            string result = GetBaskets(token); // Calls to GetBaskets Method for list of Baskets &  basket metadata under account
            var jsonObject = JsonConvert.DeserializeObject(result);
            File.WriteAllText(String.Format(@"{0}\Baskets.json", DesktopLocation), JsonConvert.SerializeObject(jsonObject, Formatting.Indented));

            System.Threading.Thread.Sleep(1000);

            PostOrders postObject = new PostOrders();

            string postResult = PostOrders(token, BasketId); // Calls PostOrders method to post an order to basket (specified by BasketId)
            postObject = JsonConvert.DeserializeObject<PostOrders>(postResult);
            File.WriteAllText(String.Format(@"{0}\Execute.json", DesktopLocation), JsonConvert.SerializeObject(postObject, Formatting.Indented));


            PostOrders orderStatus = new PostOrders();
            bool orderCompleted = false;
            while (!orderCompleted) // while loop to check status of the order. When order's dateFinished is not Null, loop is exited. 
            {
                System.Threading.Thread.Sleep(1000);
                string getOrdersResult = GetOrderStatus(token, postObject.orderId); // uses the orderId returned from call to PostOrders method to check if order is done
                orderStatus = JsonConvert.DeserializeObject<PostOrders>(getOrdersResult);
                //File.WriteAllText(String.Format(@"{0}\checkOrderStatus.json", DesktopLocation), JsonConvert.SerializeObject(orderStatus, Formatting.Indented));

                if (orderStatus.dateFinished != null)
                {
                    orderCompleted = true;
                }
            }

            System.Threading.Thread.Sleep(1000);

            Stream orderStream = GetOrderStream(token, BasketId); // Calls GetOrderSteam method using BasketId to return ordered basket's contents

            using (var fs = new FileStream(String.Format(@"{0}\{1}", DesktopLocation, FileName), FileMode.Create))
            {
                orderStream.CopyTo(fs); // Writes ordered basket contents to file specified by "FileName"
            }


        } // This is the end of the Main method. Following code represents the inidividual methods called in Main method. 

        /// <summary>
        /// Returns a data series in JSON
        /// </summary>
        /// <param name="token">OAuth 2.0 bearer token</param>
        /// <param name="mnemonic">Mnemonic - the data series' unique identifier</param>
        /// <returns></returns>
        public static string GetSingleSeries(string token, string mnemonic)
        {
            string json;

            // encode mnemonic to make it url safe
            // e.g. mnemonics that contain a "%"
            mnemonic = Uri.EscapeUriString(mnemonic);

            Uri uri = new Uri(UriEndpoint + "series?m=" + mnemonic);
            WebRequest webRequest = WebRequest.Create(uri);
            webRequest.Method = "GET";
            webRequest.Headers.Add("Authorization", "Bearer " + token);

            WebResponse webResponse = webRequest.GetResponse();

            using (Stream stream = webResponse.GetResponseStream())
            {
                using (StreamReader streamReader = new StreamReader(stream))
                {
                    json = streamReader.ReadToEnd();
                }
            }

            return json;
        }

        // GetBaskets Method will:
        // Make GET call to endpoint to retrieve basket list & basket metadata
        // Http call response as json object
        public static string GetBaskets(string token)
        {
            string json;

            Uri uri = new Uri(UriEndpoint + "baskets");
            WebRequest webRequest = WebRequest.Create(uri);
            webRequest.Method = "GET";
            webRequest.Headers.Add("Authorization", "Bearer " + token);

            WebResponse webResponse = webRequest.GetResponse();

            using (Stream stream = webResponse.GetResponseStream())
            {
                using (StreamReader streamReader = new StreamReader(stream))
                {
                    json = streamReader.ReadToEnd();
                }
            }

            return json;
        }


        // PostOrders method  will :
        // Make POST call to endpoint to order a basket (using BasketId)
        // Http call response is returned as JSON

        public static string PostOrders(string token, string BasketId)
        {
            string json;

            Uri uri = new Uri(UriEndpoint + "orders" + "?id=" + BasketId + "&type=baskets&action=run");
            WebRequest webRequest = WebRequest.Create(uri);
            webRequest.Method = "POST";
            webRequest.Headers.Add("Authorization", "Bearer " + token);
            webRequest.ContentLength = 0;

            WebResponse webResponse = webRequest.GetResponse();

            using (Stream stream = webResponse.GetResponseStream())
            {
                using (StreamReader streamReader = new StreamReader(stream))
                {
                    json = streamReader.ReadToEnd();
                }
            }

            return json;
        }

        // GetOrderStatus method  will:
        // Make GET call to endpoint to retrieve order metadata
        // http call response is returned as JSON
        //
        public static string GetOrderStatus(string token, string orderId)
        {
            string json;

            Uri uri = new Uri(UriEndpoint + "orders/" + orderId);
            WebRequest webRequest = WebRequest.Create(uri);
            webRequest.Method = "GET";
            webRequest.Headers.Add("Authorization", "Bearer " + token);

            WebResponse webResponse = webRequest.GetResponse();

            using (Stream stream = webResponse.GetResponseStream())
            {
                using (StreamReader streamReader = new StreamReader(stream))
                {
                    json = streamReader.ReadToEnd();
                }
            }

            return json;
        }
        // GetOrderStream method will :
        // 		Make GET call to endpoint to contents of ordered basket (using BasketId)
        // 		Assigns response to stream
        public static Stream GetOrderStream(string token, string BasketId)
        {
            Uri uri = new Uri(UriEndpoint + "orders" + "?id=" + BasketId + "&type=baskets");
            WebRequest webRequest = WebRequest.Create(uri);
            webRequest.Method = "GET";
            webRequest.Headers.Add("Authorization", "Bearer " + token);

            WebResponse webResponse = webRequest.GetResponse();

            Stream stream = webResponse.GetResponseStream();


            return stream;
        }

        // GetOAuthToken method will:
        //		POST the access key and encryption key to the OAuth 2.0 token endpoint
        //		Return the bearer access token, which is valid for one hour
        // The returned token is passed to every other method as the "token" argument.
        public static string GetOAuthToken(string accessKey, string encryptionKey)
        {
            string json;
            string body = "client_id=" + accessKey +
                          "&client_secret=" + encryptionKey +
                          "&grant_type=client_credentials";
            byte[] bodyBytes = Encoding.UTF8.GetBytes(body);

            Uri uri = new Uri(UriEndpoint + "oauth2/token");
            WebRequest webRequest = WebRequest.Create(uri);
            webRequest.Method = "POST";
            webRequest.ContentType = "application/x-www-form-urlencoded";
            webRequest.ContentLength = bodyBytes.Length;

            using (Stream requestStream = webRequest.GetRequestStream())
            {
                requestStream.Write(bodyBytes, 0, bodyBytes.Length);
            }

            WebResponse webResponse = webRequest.GetResponse();

            using (Stream stream = webResponse.GetResponseStream())
            {
                using (StreamReader streamReader = new StreamReader(stream))
                {
                    json = streamReader.ReadToEnd();
                }
            }

            // Deserialize the JSON response and return the access_token field.
            dynamic tokenResponse = JsonConvert.DeserializeObject(json);
            return (string)tokenResponse.access_token;
        }


    }
}
