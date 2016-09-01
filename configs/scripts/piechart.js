<script>
  window.onload = function myd() {
  document.getElementById('clickonstartMain').click()
  };
</script>

<script src="https://www.google.com/jsapi"></script>
<script>
google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawChart);
function drawChart() {
var data = google.visualization.arrayToDataTable([
['Результат', 'Процент сборок'],
['Успех', {ScriptSuccessAll}],
['Провал', {ScriptFailAll}]
]);
var options = {
title: 'Здоровье системы, %',
pieSliceText: 'none',
pieHole: 0.45,
pieSliceTextStyle: {
color: 'black',
fontSize: 10,
},
slices: {
0: { color: '#90EE90' },
1: { color: '#FA8072' }
}
};
var chart = new google.visualization.PieChart(document.getElementById('All'));
chart.draw(data, options);
}
</script>
<script type="text/javascript">
function sh() {
var obj = document.getElementById("info");
if (obj.style.display == "none" ) {
obj.style.display = "block";
}
else obj.style.display = "none";
}
</script>
<a href="javascript:sh()">Диаграмма успеха</a><br />
<div id="info" style="display: none;">
<table border="0" style="display: block;"><tr><td>
<div id="All" style="width: 300px; height: 180px;"></div>
</td><td>
<div id="Main" style="width: 300px; height: 180px;"></div>
</td></tr></table>
</div>