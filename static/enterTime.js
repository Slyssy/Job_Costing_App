// Select Employee Name
var employees = dropdown_dict.employee_list.map(d =>d.name);
var ele = document.getElementById("name");
for(var i = 0; i < employees.length; i++) {
  var opt = employees[i];

  var el = document.createElement("option");
  el.text = opt;
  el.value = opt;

  ele.add(el);
};


