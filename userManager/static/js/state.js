window.addEventListener('DOMContentLoaded', (event) => {
    if(JSON.parse(localStorage.getItem('myState'))){
      let myData = JSON.parse(localStorage.getItem('myState'))

      if(myData["state"] == "buyer") {
        window.location.href = '/buyer'
      }
      else if(myData["state"] == "maker") {
        window.location.href = '/maker'
      }
      else {
        if(!/login_user_buyer||login_user_maker/.test(window.location.href)){
          window.location.href = '/login_user_buyer'
        }
      }
    }
 });

function setState(state){
    window.localStorage.setItem('myState', state);
}

function deleteState(){
    window.localStorage.setItem('myState', '')
}
