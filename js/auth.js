const firebaseConfig = {
  apiKey: "AIzaSyBWjApTBscDteVFe2MTAmEkCT5wZSrUxZE",
  authDomain: "tank-gps-61f21.firebaseapp.com",
  projectId: "tank-gps-61f21",
  storageBucket: "tank-gps-61f21.appspot.com",
  messagingSenderId: "755394694170",
  appId: "1:755394694170:web:cf61ceadd8057be68055a3"
};

const app = firebase.initializeApp(firebaseConfig);
const auth = firebase.auth()
const database = firebase.database()

function Register() {
  email = document.getElementById('email').value
  id = document.getElementById('tanker_id').value
  password = document.getElementById('password').value
  confirm_password = document.getElementById('confirm_password').value
  console.log(email);
  if (password != confirm_password)
  alert("Password and Confirmation Password didn't match");
  else {
    auth.createUserWithEmailAndPassword(email, password)
    .then(function() {
      var user = auth.currentUser
      var database_ref = database.ref()
      var user_data = {
        email : email,
        tanker_id: id,
      }
      database_ref.child('users/' + user.uid).set(user_data)
      alert('User Created!!')
      document.getElementById('email').value = ""
      document.getElementById('tanker_id').value = ""
      document.getElementById('password').value = ""
      document.getElementById('confirm_password').value = ""
    })
    .catch(function(error) {
      var error_code = error.code
      var error_message = error.message
      alert(error_message)
    })
  } 
  return false;
}

function login () {
  email = document.getElementById('email').value
  password = document.getElementById('password').value

  auth.signInWithEmailAndPassword(email, password)
  .then(function() {
    var user = auth.currentUser
    var database_ref = database.ref()
    window.location.href='map.html'
    document.getElementById('email').value = ""
    document.getElementById('password').value = ""
  })
  .catch(function(error) {
    var error_code = error.code
    var error_message = error.message
    alert(error_message)
  })
  return false;
}

