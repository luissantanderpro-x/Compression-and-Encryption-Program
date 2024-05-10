PyCriptik

Description: A file processing tool that has features such as compression, encryption, and decryption. 

Current Features 
----------------------------
### Compression
- compresses files or directories using the following compression schemes. 
  - RAR - invoking WinRAR if available. 
  - ZIP
  - TAR 

### Encryption 
- Encryption using SHA-256 algorithm with password protect. 
- Obfuscate encrypted file name to make encrypted files appear random.

### Decryption 
- Decryption of encrypted data. 

How To Run 
----------------------------
py main.py 

Future features to be added:
----------------------------
- cross platform compatibility with Mac OS X, Linux and Windows. 
- Different encryption algorithms. 
- Different compression schemes. 
- appending encrypted information about methods of encryption, salt, and other important data that were used initially to encrypt file where just password is needed to decrypt data. 
- different compression methods aside from RAR. 
- Further code testing, error detection and announcement of said errors to the client. 