// Function to handle sign-up
async function signUp(event) {
    event.preventDefault();
    const formData = new FormData(document.getElementById("signup-form"));
    const response = await fetch("/signup", {
        method: "POST",
        body: formData
    });
    const result = await response.json();
    alert(result.message);
}

// Function to handle sign-in
async function signIn(event) {
    event.preventDefault();
    const formData = new FormData(document.getElementById("signin-form"));
    const response = await fetch("/signin", {
        method: "POST",
        body: formData
    });
    const result = await response.json();
    if (result.success) {
        alert(`Sign-in successful! Your Daisy Chain Password is: ${result.daisy_password}`);
        document.getElementById("daisy-password").value = result.daisy_password;
    } else {
        alert(result.message);
    }
}

// Function to access secure codes
async function accessSecureCodes(event) {
    event.preventDefault();
    const formData = new FormData(document.getElementById("secure-form"));
    const response = await fetch("/secure", {
        method: "POST",
        body: formData
    });
    const result = await response.json();
    if (result.success) {
        let codes = "Professional Codes:\n";
        for (const [key, value] of Object.entries(result.codes)) {
            codes += `${key}: ${value}\n`;
        }
        alert(codes);
    } else {
        alert(result.message);
    }
}