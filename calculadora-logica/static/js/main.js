/**
 * Generate selected V/F variables
 */
function getLetters() {
  let formula = document.getElementById("formulaInput").value;
  let arrayLetters = extractLetters(formula);

  let variableCard = document.getElementById("variableCard");
  variableCard.style.display = "block";

  let variablesContainer = document.getElementById("variablesContainer");
  variablesContainer.innerHTML = "";

  arrayLetters.forEach((element) => {
    let newItem = `<div class="col-md-4 mb-1">
                            <div class="form-floating">
                                <select class="form-select" id="value_${element}" aria-label="Floating label select example">
                                    <option selected value="NA">V/F</option>
                                    <option value="V">V</option>
                                    <option value="F">F</option>
                                </select>
                                <label for="value_${element}">${element}</label>
                            </div>
                        </div>`;

    variablesContainer.innerHTML += newItem;
  });
}

/**
 * Return or sets an array of non-repeating letters
 * @param {*} formula
 * @returns Array of letters
 */
function extractLetters(formula) {
  // Response array of non-repeating letters
  let letters = new Array();

  // An array of letters is obtained from the formula using regular expressions
  let purgeFormula = formula.match(/[a-zA-Z]/g);

  // Si purgeFormula está vacío o null, retorna un array vacío
  if (!purgeFormula || purgeFormula.length === 0) {
    return [];
  }

  for (let index = 0; index < purgeFormula.length; index++) {
    const element = purgeFormula[index];

    // Push in array only letters not included
    if (!letters.includes(element)) {
      letters.push(element);
    }
  }

  return letters;
}

async function executeOperation() {
  let container = document.getElementById("variablesContainer");
  let selects = container.getElementsByTagName("select");
  let values = [];

  for(let i = 0; i < selects.length; i++) {
    values.push(selects[i].value);
  }

  let formula = document.getElementById("formulaInput").value;

  const settings = {
    method: "POST",
    headers: {
      "Accept": "*/*",
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `formula=${formula}&valores=${values.join("")}`
  };
  console.log(formula, "formula");
  console.log(JSON.stringify({
      formula: formula,
    }));

  const testRequest = await fetch(`https://1d20a025-0484-4db8-bd7b-9ae5e773c4ef-00-1cyitjkouecc8.kirk.replit.dev/formula`, settings);
  const responseRequest = await testRequest.json();

  if (responseRequest.error) {
    console.error(responseRequest.error);
    return;
  }

  let tableData = responseRequest.response;
  //console.log(tableData);
  console.log(responseRequest)
  document.getElementById("resultado").innerHTML = responseRequest.test;
  return tableData;
}

function loadGrid(tableData) {
  let table = document.getElementById("tableContent");
  table.innerHTML = "";

  for (let i = 0; i < tableData.length; i++) {
    let row = table.insertRow(i);

    for (let j = 0; j < tableData[i].length; j++) {
      let cell = row.insertCell(j);
      //console.log(tableData[i][j],"----------")
      if(i < 1) {
        cell.appendChild(document.createTextNode(tableData[i][j]))
      } else {
        cell.appendChild(document.createTextNode(tableData[i][j] == "True" ? "V" : "F"));
      }
    }
  }
}

async function getTableFull() {
  let table = await executeOperation();
  loadGrid(table);
}

function setLetter(letter) {
  let formulaInput = document.getElementById("formulaInput");
  let textFormula = formulaInput.value;

  textFormula += letter;

  formulaInput.value = textFormula;
}

async function getTrueValue() {
  let arraySelect = document.getElementsByTagName("select");

  let contado = 0;
  let userTrueValues = "";
  let caseTrue = "";
  let currentCase = new Array();

  for (let index = 0; index < arraySelect.length; index++) {
    const element = arraySelect[index];

    var value = element.options[element.selectedIndex].value;

    if (value != "NA") {
      contado++;

      userTrueValues += value;
    }
  }

  if (contado != arraySelect.length) {
    alert("Por favor seleccione los valores de verdad para todos los términos");
    return;
  }

  let table = await executeOperation();
  let countRow = 0;

  table.forEach((item) => {
    if (countRow > 0) {
      let countField = 0;
      item.forEach((field) => {
        if (countField < contado) {
          caseTrue += field;
        }
        countField++;
      });
      console.log(caseTrue, "-", userTrueValues);
      if (caseTrue == userTrueValues) {
        currentCase.push(item);
      }

      caseTrue = "";
    } else {
      currentCase.push(item);
    }

    countRow++;
  });

  loadGrid(currentCase);
}

// Validations
function lettersOnly(e) {
  //only allow a-z, A-Z, with only 1 consecutive comma ...
  if (!e.key.match(/[a-zA-Z]/)) {
    e.preventDefault();
  }
}
