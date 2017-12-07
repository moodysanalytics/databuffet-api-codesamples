using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace APICodeSample
{
    class PostOrders
    {
        public string orderId { get; set; }
        public string dateOrdered { get; set; }
        public string dateStarted { get; set; }
        public string dateFinished { get; set; }
        public int failedAttempts { get; set; }
        public bool processing { get; set; }
        public int queueStatus { get; set; }
        public string basketId { get; set; }
        public int orderType { get; set; }
        public string enteredQueue { get; set; }
        public string updatedQueue { get; set; }


    }
}
