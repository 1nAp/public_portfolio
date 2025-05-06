This is an Amazon price checker that scrapes a specific page on Amazon for product title and price amount, then if the amount is below a particular threshold (in this case $ 100.00), it will send an email to a recipient with the title of the product, the price of the product, as well as a link to the product.

I use environmental variables to hide emails and smtp data, rendering the code useless.

The .env file would contain the following:

SMTP_ADDRESS= your smtp address (e.g. smtp.gmail.com)

EMAIL_ADDRESS= your email address

EMAIL_PASSWORD= your email app password

In my case, the sender and recipient emails are the same.
