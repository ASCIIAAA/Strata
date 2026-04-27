public class BankSystem {
    public void processTransaction() {
        Database db = new Database();
        db.saveData(); // This is a MethodInvocation
    }
}

public class Database {
    public void saveData() {
        System.out.println("Saved");
    }
}