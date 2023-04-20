// MULTIPLE STEPS - PREFERENCES FORM
// code adapted from https://designmodo.com/bootstrap-5-form/ 

let step = document.getElementsByClassName('step');
let prevBtn = document.getElementById('prev-btn');
let nextBtn = document.getElementById('next-btn');
let submitBtn = document.getElementById('submit-btn');
let form = document.getElementsByTagName('form')[0];
let preloader = document.getElementById('preloader-wrapper');
let bodyElement = document.querySelector('body');
let succcessDiv = document.getElementById('success');

form.onsubmit = () => {
    replace_function()
    return false
}

let current_step = 0;
let stepCount = 3;

step[current_step].classList.add('d-block');
if (current_step == 0) {
    prevBtn.classList.add('d-none');
    submitBtn.classList.add('d-none');
    nextBtn.classList.add('d-inline-block');
}

const progress = (value) => {
    document.getElementsByClassName('progress-bar')[0].style.width = `${value}%`;
}

nextBtn.addEventListener('click', () => {
    current_step++;
    let previous_step = current_step - 1;
    if ((current_step > 0) && (current_step <= stepCount)) {
        prevBtn.classList.remove('d-none');
        prevBtn.classList.add('d-inline-block');
        step[current_step].classList.remove('d-none');
        step[current_step].classList.add('d-block');
        step[previous_step].classList.remove('d-block');
        step[previous_step].classList.add('d-none');
        if (current_step == stepCount) {
            submitBtn.classList.remove('d-none');
            submitBtn.classList.add('d-inline-block');
            nextBtn.classList.remove('d-inline-block');
            nextBtn.classList.add('d-none');
        }
    } 
    else {
        if (current_step > stepCount) {
            form.onsubmit = () => {
                return true
            }
        }
    }
    store_checkbox_value()
    progress((100 / stepCount) * current_step);
});
 
prevBtn.addEventListener('click', () => {
    if (current_step > 0) {
        current_step--;
        let previous_step = current_step + 1;
        prevBtn.classList.add('d-none');
        prevBtn.classList.add('d-inline-block');
        step[current_step].classList.remove('d-none');
        step[current_step].classList.add('d-block')
        step[previous_step].classList.remove('d-block');
        step[previous_step].classList.add('d-none');
        if (current_step < stepCount) {
            submitBtn.classList.remove('d-inline-block');
            submitBtn.classList.add('d-none');
            nextBtn.classList.remove('d-none');
            nextBtn.classList.add('d-inline-block');
            prevBtn.classList.remove('d-none');
            prevBtn.classList.add('d-inline-block');
        }
    }
 
    if (current_step == 0) {
        prevBtn.classList.remove('d-inline-block');
        prevBtn.classList.add('d-none');
    }
    progress((100 / stepCount) * current_step);
});

// function getting the values selected in the checkboxes
function store_checkbox_value() {
    let checkboxes = document.querySelectorAll("input[type='checkbox']:checked");
    let selected_options = [];

    checkboxes.forEach(checkbox => {
        selected_options.push(checkbox.value)
    })
    
    let amount_cash = document.getElementById('cash_day')   // get the value in the range
    selected_options.push(amount_cash.value) 

    // const s = JSON.stringify(selected_options);  // s is a list 
    console.log(selected_options);  // -----------!!!!!!!!! can be removed later - it prints the values in the console on the browser and terminal  !!!!!!!!!!!-----------------
    // window.alert(selected_options)  // -----------!!!!!!!!! can be removed later - alert window on the browser !!!!!!!!!!!-----------------------

    // sends an AJAX request to the server with the values selected in the checkboxes
    $.ajax({
        type: "POST",
        url: "/preferences",
        data: JSON.stringify(selected_options),
        contentType: "application/json",
        dataType: "json"
    })
};


// function replacing the URL and the user can't go back the previous page (once left the preferences form)
function replace_function(){
    window.location.replace("plan");
}
 

 

// submitBtn.addEventListener('click', () => {
//     preloader.classList.add('d-block');
 
//     const timer = ms => new Promise(res => setTimeout(res, ms));
 
//     timer(3000)
//         .then(() => {
//             bodyElement.classList.add('loaded');
//         }).then(() => {
//             step[stepCount].classList.remove('d-block');
//             step[stepCount].classList.add('d-none');
//             prevBtn.classList.remove('d-inline-block');
//             prevBtn.classList.add('d-none');
//             submitBtn.classList.remove('d-inline-block');
//             submitBtn.classList.add('d-none');
//             succcessDiv.classList.remove('d-none');
//             succcessDiv.classList.add('d-block');
//         })
 
// });



// RANGE
// code from https://css-tricks.com/value-bubbles-for-range-inputs/

const allRanges = document.querySelectorAll(".range-wrap");
allRanges.forEach(wrap => {
  const range = wrap.querySelector(".range");
  const bubble = wrap.querySelector(".bubble");

  range.addEventListener("input", () => {
    setBubble(range, bubble);
  });
  setBubble(range, bubble);
});

function setBubble(range, bubble) {
  const val = range.value;
  const min = range.min ? range.min : 0;
  const max = range.max ? range.max : 100;
  const newVal = Number(((val - min) * 100) / (max - min));
  bubble.innerHTML = ("$ " + val);

  bubble.style.left = `calc(${newVal}% + (${8 - newVal * 0.15}px))`;
}


// const formulaire = document.querySelector('#formPlan');
// const dropDownButton = document.querySelector('#dropdown-title');
// const buttonsOptions = document.querySelectorAll('.dropdown-item');
// const buttonsOption = document.querySelectorAll('.dropdown-props');

// buttonsOption.addEventListener('click', event => {
//   event.preventDefault()
//   console.log(buttonsOptions);
// });

// for (const button of buttonsOptions) {
//   button.addEventListener('click', event => {
//     event.preventDefault()
//     dropDownButton.textContent = event.target.value;
//   });
// }

// formulaire.addEventListener("submit", e => e.preventDefault())




