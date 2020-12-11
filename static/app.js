// Search Table
$("#dashboard_search").on("keyup", function () {
  let value = $(this).val();
  console.log("Value:", value);
  let data = searchTable(value, project_list);
  buildTable(data);
});



function searchTable(value, data) {
  let filteredData = [];

  for (const item in data) {
    value = value.toLowerCase();
    let name = data[item].project_name.toLowerCase();

    if (name.includes(value)) {
      filteredData.push(data[item]);
    }
  }

  return filteredData;
}


// Begin Build Table Javascript
buildTable(project_list);

function buildTable(data) {
  let table = document.getElementById("dashboardTable");

  table.innerHTML = "";

  for (const item in data) {
    var row = `<tr>

                        <td><a href="/search?project_id=${data[item].id}">${data[item].project_name}</a></td>

                        <td>$ ${data[item].fin_act_revenue}</td>
                        <td>${data[item].fin_est_labor_hours}</td>
                        <td>${data[item].fin_act_labor_hours}</td>
                        <td>$ ${data[item].fin_est_labor_expense}</td>
                        <td>$ ${data[item].fin_act_labor_expense}</td>
                        <td>${data[item].act_start_date}</td>
                   </tr>`;

    table.innerHTML += row;
  }
}
for (const item in project_list) {
    // console.log(item)
  // console.log(project_list[item])
}


