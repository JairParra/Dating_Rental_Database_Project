-- 1. A mate want to accept a request. Assume the request id is 101.
UPDATE request 
SET rstatus = 'accepted'
WHERE rid = 101;

-- 2. A customer pays for an invoice and the invoice status is updated to paid.
-- Assume the invoice id is 10.
UPDATE invoice 
SET status = 'paid'
WHERE inid = 10;

-- 3. A customer wants to update his/her email to "xzy@mail.mcgill.ca"
-- Assume the email of this customer account is cchittem1b@amazon.de.
UPDATE usertable
SET email = 'xzy@mail.mcgill.ca'
WHERE email = 'cchittem1b@amazon.de';

-- 4. Because of an term change of ApplePay service, our company is not allowed to keep
-- any payment data with ApplePay anymore. We want to delete all the invoice that is paid using ApplePay

DELETE FROM invoice
WHERE method = 'applepay';