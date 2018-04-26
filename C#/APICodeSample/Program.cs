using System;
using System.IO;
using System.Net;
using System.Text;
using System.Security.Cryptography;
using Newtonsoft.Json;
// Newtonsoft.Json used for serializing & deserializing JSON objects

namespace APICodeSample
{
    class Program
    {
        private const string UriEndpoint = "https://api.economy.com/data/v1/";
        private const string AccessKeyHeader = "AccessKeyId";
        private const string SignatureHeader = "Signature";
        private const string TimeStampHeader = "TimeStamp";
        private const string AccessKey = ""; // Enter Your Access Key
        private const string EncryptionKey = ""; // Enter Your Encryption Key


        // This Main method calls on subsequent methods to perform the following tasks
        // Get list of baskets, post an order to a basket, check the order status and retreive the contents of the ordered basket once completed
        static void Main(string[] args)
        {
            string BasketId = ""; //BasketId of basket you want to run 
            string FileName = ""; // Enter Filename that basket contents will be written to
            string DesktopLocation = Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory); //All logs and basket files are currently saved to the Desktop


            string singleSeries = GetSingleSeries(AccessKey, EncryptionKey, "ET.IUSA");
            var jsonSingleSeries = JsonConvert.DeserializeObject(singleSeries);
            File.WriteAllText(String.Format(@"{0}\SingleSeries.json", DesktopLocation), JsonConvert.SerializeObject(jsonSingleSeries, Formatting.Indented));

            string result = GetBaskets(AccessKey, EncryptionKey); // Calls to GetBaskets Method for list of Baskets &  basket metadata under account
            var jsonObject = JsonConvert.DeserializeObject(result);
            File.WriteAllText(String.Format(@"{0}\Baskets.json", DesktopLocation), JsonConvert.SerializeObject(jsonObject, Formatting.Indented));

            System.Threading.Thread.Sleep(1000);

            PostOrders postObject = new PostOrders();

            string postResult = PostOrders(AccessKey, EncryptionKey, BasketId); // Calls PostOrders method to post an order to basket (specified by BasketId)
            postObject = JsonConvert.DeserializeObject<PostOrders>(postResult);
            File.WriteAllText(String.Format(@"{0}\Execute.json", DesktopLocation), JsonConvert.SerializeObject(postObject, Formatting.Indented));


            PostOrders orderStatus = new PostOrders();
            bool orderCompleted = false;
            while (!orderCompleted) // while loop to check status of the order. When order's dateFinished is not Null, loop is exited. 
            {
                System.Threading.Thread.Sleep(1000);
                string getOrdersResult = GetOrderStatus(AccessKey, EncryptionKey, postObject.orderId); // uses the orderId returned from call to PostOrders method to check if order is done
                orderStatus = JsonConvert.DeserializeObject<PostOrders>(getOrdersResult);
                //File.WriteAllText(String.Format(@"{0}\checkOrderStatus.json", DesktopLocation), JsonConvert.SerializeObject(orderStatus, Formatting.Indented));

                if (orderStatus.dateFinished != null)
                {
                    orderCompleted = true;
                }
            }

            System.Threading.Thread.Sleep(1000);

            Stream orderStream = GetOrderStream(AccessKey, EncryptionKey, BasketId); // Calls GetOrderSteam method using BasketId to return ordered basket's contents

            using (var fs = new FileStream(String.Format(@"{0}\{1}", DesktopLocation, FileName), FileMode.Create))
            {
                orderStream.CopyTo(fs); // Writes ordered basket contents to file specified by "FileName"
            }


        } // This is the end of the Main method. Following code represents the inidividual methods called in Main method. 

        /// <summary>
        /// Returns a data series in JSON
        /// </summary>
        /// <param name="accessKey">Access Key</param>
        /// <param name="encryptionKey">Encryption Key</param>
        /// <param name="mnemonic">Mnemonic - the data series' unique identifier</param>
        /// <returns></returns>
        public static string GetSingleSeries(string accessKey, string encryptionKey, string mnemonic)
        {
            string timeStamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ");
            string signature = CreateHMACSignature(accessKey, encryptionKey, timeStamp);
            string json;

            // encode mnemonic to make it url safe
            // e.g. mnemonics that contain a "%"
            mnemonic = Uri.EscapeUriString(mnemonic);

            Uri uri = new Uri(UriEndpoint + "series?m=" + mnemonic);
            WebRequest webRequest = WebRequest.Create(uri);
            webRequest.Method = "GET";
            webRequest.Headers.Add(AccessKeyHeader, accessKey);
            webRequest.Headers.Add(TimeStampHeader, timeStamp);
            webRequest.Headers.Add(SignatureHeader, signature);

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
        // Generate new timeStamp & signature
        // Make GET call to endpoint to retrieve basket list & basket metadata	
        // Http call response as json object 
        public static string GetBaskets(string accessKey, string encryptionKey)
        {
            string timeStamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ");
            string signature = CreateHMACSignature(accessKey, encryptionKey, timeStamp);
            string json;

            Uri uri = new Uri(UriEndpoint + "baskets");
            WebRequest webRequest = WebRequest.Create(uri);
            webRequest.Method = "GET";
            webRequest.Headers.Add(AccessKeyHeader, accessKey);
            webRequest.Headers.Add(TimeStampHeader, timeStamp);
            webRequest.Headers.Add(SignatureHeader, signature);

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
        // Generate new timestamp and signature 
        // Make POST call to endpoint to order a basket (using BasketId)
        // Http call response is returned as JSON

        public static string PostOrders(string accessKey, string encryptionKey, string BasketId)
        {
            string timeStamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ");
            string signature = CreateHMACSignature(accessKey, encryptionKey, timeStamp);
            string json;

            Uri uri = new Uri(UriEndpoint + "orders" + "?id=" + BasketId + "&type=baskets&action=run");
            WebRequest webRequest = WebRequest.Create(uri);
            webRequest.Method = "POST";
            webRequest.Headers.Add(AccessKeyHeader, accessKey);
            webRequest.Headers.Add(TimeStampHeader, timeStamp);
            webRequest.Headers.Add(SignatureHeader, signature);
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
        // Generate new timestamp & signature
        // Make GET call to endpoint to retrieve order metadata 
        // http call response is returned as JSON 
        // 
        public static string GetOrderStatus(string accessKey, string encryptionKey, string orderId)
        {
            string timeStamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ");
            string signature = CreateHMACSignature(accessKey, encryptionKey, timeStamp);
            string json;

            Uri uri = new Uri(UriEndpoint + "orders/" + orderId);
            WebRequest webRequest = WebRequest.Create(uri);
            webRequest.Method = "GET";
            webRequest.Headers.Add(AccessKeyHeader, accessKey);
            webRequest.Headers.Add(TimeStampHeader, timeStamp);
            webRequest.Headers.Add(SignatureHeader, signature);

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
        // 		Generate new timeStamp & signature
        // 		Make GET call to endpoint to contents of ordered basket (using BasketId)
        // 		Assigns response to stream
        public static Stream GetOrderStream(string accessKey, string encryptionKey, string BasketId)
        {
            string timeStamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ");
            string signature = CreateHMACSignature(accessKey, encryptionKey, timeStamp);

            Uri uri = new Uri(UriEndpoint + "orders" + "?id=" + BasketId + "&type=baskets");
            WebRequest webRequest = WebRequest.Create(uri);
            webRequest.Method = "GET";
            webRequest.Headers.Add(AccessKeyHeader, accessKey);
            webRequest.Headers.Add(TimeStampHeader, timeStamp);
            webRequest.Headers.Add(SignatureHeader, signature);

            WebResponse webResponse = webRequest.GetResponse();

            Stream stream = webResponse.GetResponseStream();


            return stream;
        }

        //CreateHMACSignature Method will: 
        //		Create & return signature 
        // 		This method is used in all preceeding methods except main method  
        public static string CreateHMACSignature(string accessKey, string encryptionKey, string timeStamp)
        {
            string signature = string.Empty;
            byte[] keyBytes = Encoding.UTF8.GetBytes(encryptionKey);
            using (HMAC hmac = new HMACSHA256(keyBytes))
            {
                byte[] bytesToHash = Encoding.UTF8.GetBytes(accessKey + timeStamp);
                byte[] hashedBytes = hmac.ComputeHash(bytesToHash);
                for (int i = 0; i < hashedBytes.Length; i++)
                {
                    signature += hashedBytes[i].ToString("X2");
                }
            }
            return signature;
        }


    }
}
