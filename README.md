# Description
This python project emulates a blockchain network and replicates all the operations of a blockchain network.

Blocks, keys, transancations, signatures, signing transactions, hashing are all simulated by this simple blockchain network project 

# Getting started
**Activate the virtual environment**
```
source blockchain-env/scripts/activate
```

**Install all packages**
```
pip install -r REQUIREMENTS.txt
```

**Run the tests**
 
 Make sure to activate the virtual environment

 ```
 python -m pytest Backend/Tests
 ```

**Run the application and API**

 Make sure to activate the virtual environment
 ```
 python -m Backend.App
 ```

 **Run a PEER instance**
 Make sure to activate the virtual environment
 ```
 export PEER=True && python -m Backend.App
 ```

 **Run the frontend**
 In the frontend directory:
 ```
 npm run start
 ```

 **Seed the backend with data**
  Make sure to activate the virtual environment
  ```
  export SEED_DATA=True && python -m Backend.App
  ```
