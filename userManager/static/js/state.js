/**
 * Check localstorage state, users push or not
 * states: ['buyer', 'maker']
 * Send to application depend in state.
 */
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

// Create new state in localstorage
function setState(state){
    window.localStorage.setItem('myState', state);    
}

// Delate state and redirect 
function deleteState(){
    let state = window.localStorage.getItem("myState")
    window.localStorage.setItem('myState', '')
    window.location.href = `/login_user_${state}`
}
