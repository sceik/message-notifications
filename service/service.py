from nameko.rpc import rpc, RpcProxy
import sqlite3
import logging
from datetime import date, datetime
import re

class Message(object):
    name = "message"  

    @rpc
    def message(self, text):
        logging.info("Process message: %s", text)
        conn = sqlite3.connect('store')

        # Find customers in text
        customers = []
        for row in conn.execute('SELECT id, notification_label FROM customers'):
            size = len(re.findall(row[1], text))
            if (size > 0): 
                customers.append(row) 

        if len(customers) != 1:
            #Insert whitout customer ID
            logging.warning("No customer found in message: %s", text)
            conn.execute("INSERT INTO notifications('body') VALUES (?)", (text,))
        else:
            customerID = customers[0][0]
            logging.info("Customer %d found in message: %s", customerID, text)
            #Inset new notification on DB
            conn.execute("INSERT INTO notifications('body','id_customer') VALUES (?,?)", (text,customerID,))
            #Get today date
            today = date.today()
            #
            notificationCount = conn.execute('SELECT * FROM notification_counters WHERE day = ? AND id_customer = ?', (today,customerID,))
            #Get customer notifications number
            counter = notificationCount.fetchone();
            #If first customer notifications insert row
            if counter == None :
                conn.execute('INSERT INTO notification_counters VALUES(?,?,?)', (customerID,1,today))
            else:
                conn.execute('UPDATE notification_counters SET num = ? WHERE day = ? AND id_customer = ? ', (counter[1]+1,today,customerID))
        try:       
            # Save (commit) the changes
            conn.commit()
        except Exception as e:
            # Roll back any change if something goes wrong
            db.rollback()
            logging.exception("Something went wrong with DB")
        finally:
            # Close the db connection
            logging.info("Message correctly processed")
            db.close()
