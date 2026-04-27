public class LegacyOrderSystem {
    public static void main(String[] args) {
        OrderProcessor processor = new OrderProcessor();
        processor.processTransaction("TXN123", 500.0);
    }
}

class OrderProcessor {
    private Database db = new Database();
    private EmailService email = new EmailService();
    private Logger log = new Logger();
    private PaymentGateway payment = new PaymentGateway();

    // The "God Method" - handles way too many responsibilities
    public void processTransaction(String id, double amount) {
        log.info("Starting transaction: " + id);
        
        if (payment.authorize(amount)) {
            db.saveOrder(id, amount);
            email.sendConfirmation(id);
            log.info("Transaction Success");
        } else {
            log.error("Transaction Failed");
        }
    }

    // Dead Code - This is never called! 
    // Your engine should flag this as a "Ghost"
    public void deleteEverything() {
        db.clearAllRecords();
    }
}

class Database {
    public void saveOrder(String id, double amt) { /* SQL Logic */ }
    public void clearAllRecords() { /* DANGEROUS Logic */ }
}

class EmailService {
    public void sendConfirmation(String id) { /* SMTP Logic */ }
}

class PaymentGateway {
    public boolean authorize(double amount) { return true; }
}

class Logger {
    public void info(String msg) { System.out.println(msg); }
    public void error(String msg) { System.err.println(msg); }
}