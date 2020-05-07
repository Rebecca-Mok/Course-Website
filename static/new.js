// Register Page
function register(){
    alert("Please log out first before making a new account.");
    return "";
}
// Feedback Page
function added(){
    alert("Request sent.");
    return "";
}



$('#myLink').click(function(){ 
    register(); 
    return false; 
});

// Grades Page
function showDiv() {
    document.getElementById('requests').style.display = "block";
    document.getElementById('class-grades').style.display = "none";
}
function showGrades() {
    document.getElementById('requests').style.display = "none";
    document.getElementById('class-grades').style.display = "block";
}

function showStudentDiv() {
    document.getElementById('makeRequest').style.display = "block";
    document.getElementById('student-grades').style.display = "none";
}
function showStudentGrades() {
    document.getElementById('makeRequest').style.display = "none";
    document.getElementById('student-grades').style.display = "block";
}

// Redirect (redirect.html)
function toLogin(){ 
    location.href = '/'
}
function toRegister(id){
    location.href = '/register'
}
