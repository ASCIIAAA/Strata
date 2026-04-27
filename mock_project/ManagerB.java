public class ManagerB {
    public void doMoreWork() {
        // independent logic
    }
    public void callbackA() {
        ManagerA ma = new ManagerA();
        ma.callbackB();
    }
}
