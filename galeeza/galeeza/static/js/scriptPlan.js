

const formulaire = document.querySelector('#formPlan');
const dropDownButton = document.querySelector('#dropdown-title');
const buttonsOptions = document.querySelectorAll('.dropdown-item');
const arrival = document.querySelector('#arrival');
const departure = document.querySelector('#departure');

arrival.addEventListener("change", (e) => {
    arrival.value = e.target.value
    departure.setAttribute('min', e.target.value)
})

departure.addEventListener("change", (e) => {
    departure.value = e.target.value
    arrival.setAttribute('max', e.target.value)
})

buttonsOptions.forEach(button => {
  button.addEventListener('click', event => {
    dropDownButton.textContent = event.target.value;
  });
})



// formulaire.onsubmit = () => {
//     replace_function()
//     return false
// }

// formulaire.addEventListener("submit", e => {
//     e.preventDefault()
//     // replace_function()
// })

// function replacing the URL and the user can't go back the previous page (once left the preferences form)
// function replace_function(){
//     window.location.replace("profile");
// }

