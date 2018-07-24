
async function addTable() {
var myTableDiv = document.getElementById("metric_results")
var table = document.createElement('TABLE')
var tableBody = document.createElement('TBODY')

const fetchParams = {  
  method: "GET",
  mode: "cors",
  cache: "default"
};
table.border = '1'
table.appendChild(tableBody);
event_dates = ["Names"]


await fetch('http://localhost:5000/events', fetchParams)  
.then(res => {
  if (!res.ok) {
    throw new Error(res.statusText);
  }
  return res.json();
})
.then(eventdata => {
  for (i = 0; i < eventdata.length; i++) {
    rowhash = eventdata[i]
    event_dates.push(rowhash.Date)
  }

//TABLE COLUMNS
var tr = document.createElement('TR');
tableBody.appendChild(tr);
for (i = 0; i < event_dates.length; i++) {
var th = document.createElement('TH')
th.width = '75';
th.appendChild(document.createTextNode(event_dates[i]));
tr.appendChild(th);
}
})
await fetch('http://localhost:5000/attendance', fetchParams)  
.then(res => {
  if (!res.ok) {
    throw new Error(res.statusText);
  }
  return res.json();
})
.then(data => {
  let attendanceData = {}
  for (i = 0; i < data.length; i++){
    rowhash = data[i]
    console.log(rowhash)
      if (!(rowhash.Name in attendanceData)) {
        attendanceData[rowhash.Name] = [rowhash.Date]
        console.log(rowhash.Date)
        } else {
        rowhash.name = attendanceData[rowhash.Name].push(rowhash.Date)
      }

  }
//TABLE ROWS
for (var key in attendanceData) {
  var tr = document.createElement('TR');
  var td = document.createElement('TD')
  td.appendChild(document.createTextNode(key));
  tr.appendChild(td)
  console.log("Doing Name: " + key)
  for (j = 1; j < event_dates.length; j++) {
    var td = document.createElement('TD')
    if (attendanceData[key].includes(event_dates[j])) {
    td.appendChild(document.createTextNode("YES"));
    tr.appendChild(td)
    console.log("Doing yes on " + event_dates[j] + " in " + attendanceData[key])
    } else {
    td.appendChild(document.createTextNode("NO"));
    tr.appendChild(td)
    console.log("Doing no on " + event_dates[j] + " in " + attendanceData[key])
    }
  }
  tableBody.appendChild(tr);
  
  }
})
  .catch(error => {
    console.error(`Fetch Error =\n`, error);
  });

myTableDiv.appendChild(table)

}
