# FlightsBooking- Mongodb-multi-document-transactions  
  This project saving data of flights booking with commitTransaction.
  We can add\delete a flights and watch each user booked flights.

https://user-images.githubusercontent.com/49592750/192870812-fbe549b2-351c-4bcf-9375-872e7b7134c0.mp4

 ## MongoDB 
- Check ubuntu version 
  ```
  lsb_release -a
  ```
  
- Install mongod
	- https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-20-04
		- basically, update apt with a new source and install the package mongodb-org from it.
		- install mongosh as well
		
    ```
    sudo apt-get install -y mongodb-mongosh
    ```
- Setup primary instance
	- stop mongod service
		
    ```
    sudo systemctl stop mongod
    ```
    
	- open the conf file location 
    
    ```
    cd /etc/mongod.conf
    ```
    
	- look for replication section:
		- uncomment it
		- add under (enter + 2 space indentation)
			- replSetName: "replicasetname"
	- start mongod service
  
  ```
		 sudo systemctl start mongod
  ```
	
  - open mongo shell to primary instance
  
    ```
    mongosh
    ```
	- initialize replica set
		
    ```
      rs.initialize()
    ```
    
	- exit mongo shell
		  
      ```
      exit
      ```
- setup secondary instance
	- create directory for the new instance to store data
		- can be anywhere, even in your home folder
			  - mkdir ~/mongodb2
	- in a new shell, start the new instance
  
  ```
		  mongod --port 27018 --replSet replicasetname --dbpath ~/mongodb2
  ```
  
  - don't close this shell as it will stop the second instance

- connect secondary instance to the replica set
	- open mongo shell to primary instance
	
  ```
        mongosh
  ```
	- connect secondary instance to replica set
	
  ```
        rs.add('127.0.0.1:27018')
  ```
  
	- the ip is loopback, the port should match to one used to start the secondary instance
	- check everything is set up
		- run 
      
      ```
          rs.status()
      ```
		
    - see that in the result, "members" contains 2 entries: PRIMARY and SECONDARY

MongoDB’s transactions are a conversational set of related operations that must atomically commit or fully rollback 
with all-or-nothing execution.
Transactions are used to make sure operations are atomic even across multiple collections or databases.
Thus, with snapshot isolation reads, 
another user can only see all the operations or none of them.

## Python & Requirements:
      sudo apt install python3
      sudo apt install python3-pip
      pip3 install -r requirements.txt 
      
Logs:
![log](https://user-images.githubusercontent.com/49592750/192871200-63fef5b8-b247-4408-b960-feb666922d95.jpg)

Tables:
![tables](https://user-images.githubusercontent.com/49592750/192871622-127707ce-2191-43f1-adc8-180092f104eb.jpg)


