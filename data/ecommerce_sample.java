// Realistic Java E-Commerce Backend Simulation
// Designed to produce beautiful, realistic dependency graphs, detect a God Object, 
// and map out clean microservices.

public class OmniECommerceGod {
    private OrderManager orderManager;
    private PaymentGateway paymentGateway;
    private InventorySystem inventorySystem;
    private UserAuth auth;

    public void processEverything(String userId, String itemId, int amount) {
        if (auth.verifyUser(userId)) {
            if (inventorySystem.checkStock(itemId, amount)) {
                paymentGateway.charge(userId, amount);
                orderManager.createOrder(userId, itemId);
                inventorySystem.deductStock(itemId, amount);
                EmailNotifier.sendReceipt(userId);
            }
        }
    }
    
    public void manualOverride() {
        // God object method
        inventorySystem.forceUpdate();
        paymentGateway.refundAll();
    }
}

class OrderManager {
    private OrderDatabase db;
    private InvoiceGenerator invoiceGen;

    public void createOrder(String user, String item) {
        db.saveOrder(user, item);
        invoiceGen.generate(user);
    }
}

class OrderDatabase {
    public void saveOrder(String u, String i) {
        System.out.println("Saving order to DB...");
    }
}

class InvoiceGenerator {
    public void generate(String user) {
        PDFUtil.buildPDF(user);
        System.out.println("Invoice generated");
    }
}

class PaymentGateway {
    private StripeAPI stripe;
    private PayPalAPI paypal;

    public void charge(String user, int amount) {
        stripe.process(user, amount);
        TransactionLogger.log(user, amount);
    }
    
    public void refundAll() {
        System.out.println("Refunding everything!");
    }
}

class StripeAPI {
    public void process(String u, int a) {
        System.out.println("Stripe charged: " + a);
    }
}

class PayPalAPI {
    public void process(String u, int a) {
        System.out.println("PayPal processing...");
    }
}

class TransactionLogger {
    public static void log(String u, int a) {
        System.out.println("Logged transaction.");
    }
}

class InventorySystem {
    private WarehouseDB warehouse;

    public boolean checkStock(String item, int amt) {
        return warehouse.getQuantity(item) >= amt;
    }

    public void deductStock(String item, int amt) {
        warehouse.reduce(item, amt);
    }
    
    public void forceUpdate() {
        System.out.println("God mode update");
    }
}

class WarehouseDB {
    public int getQuantity(String item) {
        return 100;
    }
    public void reduce(String item, int amt) {
        System.out.println("Stock reduced");
    }
}

class UserAuth {
    private SessionManager session;

    public boolean verifyUser(String u) {
        return session.isValid(u);
    }
}

class SessionManager {
    public boolean isValid(String u) {
        return true;
    }
}

class EmailNotifier {
    public static void sendReceipt(String u) {
        SMTPClient.send(u, "Your receipt");
    }
}

class SMTPClient {
    public static void send(String to, String msg) {
        System.out.println("Email sent to " + to);
    }
}

class PDFUtil {
    public static void buildPDF(String data) {
        System.out.println("Building PDF...");
    }
}

// ---------------------------------------------------------
// Phase III: Ghost Code (Dead Code)
// These classes and methods are never called by the main system.
// ---------------------------------------------------------
class LegacyBillingSystem {
    public void processOldBilling() {
        System.out.println("This is ghost code.");
        connectToMainframe();
    }
    
    private void connectToMainframe() {
        System.out.println("Dialing up 1998...");
    }
}

class UnusedPromoCodeEngine {
    public void applyPromo() {
        System.out.println("Applying discount");
    }
}
