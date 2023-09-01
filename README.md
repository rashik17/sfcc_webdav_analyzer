## SFCC Webdav Analyzer

This script retrieves the sizes of files hosted on Salesforce Commerce Cloud (B2C) WebDAV / IMPEX. It recursively traverses through folders and subfolders, retrieves the file sizes, and writes the output to a csv. The script utilizes the Salesforce Commerce Cloud API to authenticate and access the files.

The script does not download the actual files(images, feed files), but only gets the HTTP HEAD to understand the resource's Content-Length.

## Prerequisites 
- Create an Account Manager API client id secret for Webdav access ([documentation](https://help.salesforce.com/s/articleView?id=cc.b2c_webdav_authentication_and_authorization.htm&type=5)) 
- Configure the client id with appropriate read access in the Business Manager > Administration >  Organization >  WebDAV Client Permissions ([documentation](https://help.salesforce.com/s/articleView?id=cc.b2c_web_dav_client_permissions.htm&type=5))

## Usage

1. Clone the repository.
2. Create a new .env file using .env-example as reference and provide details.
3. Open the terminal and navigate to the project directory.
4. Run the following command to install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the following command to run the script :
   ```
   python s.py
   ```
4. The CSV file will be generated in the project directory.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Author

Rashik Gupta

