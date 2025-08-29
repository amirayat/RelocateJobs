Step 0: zappa deploy production


Step 1: Add relocate.works to Rout53 Hosted Zone
    Copy NS Record in AWS Route 53 to pouyanit.com
    verify ns records by this comand
        nslookup -type=NS relocate.works


Step 2: Install Certbot & Request a Certificate with DNS Challenge
    sudo apt update
    sudo apt install certbot python3-certbot-dns-route53
    sudo certbot certonly --manual --preferred-challenges=dns -d relocate.works


Step 3: Add the TXT Record in AWS Route 53
    Go to AWS Route 53 (or your DNS provider).
    Find your hosted zone for relocate.works
    Create a TXT record:
    Name: _acme-challenge.relocate.works
    Type: TXT
    Value: (The value provided by Certbot)
    TTL: 300 (or default)


Step 4: Convert Certbot certificates to PEM format
    sudo openssl pkcs12 -export -out cert.p12 -inkey /etc/letsencrypt/live/relocate.works/privkey.pem -in /etc/letsencrypt/live/relocate.works/cert.pem -certfile /etc/letsencrypt/live/relocate.works/chain.pem


Step 5: Import into AWS Certificate Manager:
    Go to AWS ACM → Import certificate.
    Upload:
    Certificate body (cert.pem)
    Private key (privkey.pem)
    Certificate chain (chain.pem)


Step 6: Set up a Custom Domain in API Gateway
    Go to the API Gateway console in AWS.
    In the left navigation pane, choose Custom domain names.
    Click Create.
    Enter your domain name (relocate.works).
    Choose the Regional endpoint type.
    For the ACM certificate, either:
    Select an existing certificate for your domain from AWS Certificate Manager (ACM)
    Under Mapping configuration, select your API (production) and the stage (production).
    Click Save.


Step 7: Configure DNS (Route 53 or Your DNS Provider)
    If using AWS Route 53:
    Go to the Route 53 console.
    Select your hosted zone for relocate.works.
    Create a new record:
    Choose Alias
    Minimum TLS Version	TLS 1.2
    Mutual TLS Authentication	Disabled (default)
    Select IPV4 Address Type
    Select Alias to API Gateway API
    Choose the region where your API is deployed
    Select the custom domain you created
    Save the record.

