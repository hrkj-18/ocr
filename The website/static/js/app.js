function login(){

	// Get elemets
	  var txtEmail = document.getElementById('txtEmail');
	  var txtPassword = document.getElementById('txtPassword');
	  var btnLogin = document.getElementById('btnLogin');
	  var btnSignUp = document.getElementById('btnSignUp');
	  //const btnLogOut = document.getElementById('btnLogOut');

	  
	  	//get email and pass
	  	var email = txtEmail.value;
	  	var pass = txtPassword.value;
	  	var auth = firebase.auth();
	  	//sign in
	  	var promise = auth.signInWithEmailAndPassword(email, pass);
	  	promise.catch(e => console.log(e.message));
}