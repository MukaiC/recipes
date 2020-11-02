document.addEventListener('DOMContentLoaded', function() {
  var ingredientForm = document.querySelectorAll(".ingredient-form");
  var container = document.querySelector("#form-container");
  var addButton = document.querySelector("#add-form");
  var totalForms = document.querySelector("#id_recipeingredients-TOTAL_FORMS");


  //Get the number of the last form
  var formNum = ingredientForm.length-1;
  console.log(`num of last form: ${formNum}`);

  addButton.addEventListener('click', addForm);

  function addForm(e){
    //Prevent loading
    e.preventDefault();

    console.log(`initial totalForms ${totalForms}`);
    //Clone the ingredient form
    console.log(ingredientForm);
    let newForm = ingredientForm[0].cloneNode(true);

    //Create a regular expression to find and replace the form number
    let formRegex = RegExp(`recipeingredients-(\\d){1}-`, 'g');

    //Increment the form number
    formNum++;
    console.log(`formNum ${formNum}`);
    //Update the new form with the correct form number
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `recipeingredients-${formNum}-`);
    console.log(`updated newForm ${newForm.innerHTML}`);

    //Insert the new form at the end of the list of forms before the add addButton
    container.insertBefore(newForm, addButton);

    //Increment the number of total forms and set the value attribute in the management form
    totalForms.setAttribute('value', `${formNum+1}`);

    console.log(totalForms.value);

  };

});
