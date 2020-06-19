function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) 
        month = '0' + month;
    if (day.length < 2) 
        day = '0' + day;

    return [year, month, day].join('-');
}

var period = document.getElementById("period_desc").value
document.getElementById("period_desc").onchange = function() {
    period = document.getElementById("period_desc").value;
    document.getElementById("start_date").value = null;
    document.getElementById("end_date").value = null;
    document.getElementById("start_date").disabled = false;
    document.querySelectorAll('input[value="--select an option--"]').disabled = true;
    // document.getElementById("--select an option--").disabled = true;
    document.getElementById("end_date").disabled = true;
        console.log(period);
};
console.log(period)

var s_date = document.getElementById("start_date").value;
document.getElementById("start_date").onchange = function() {
    s_date = document.getElementById("start_date").value;
    s_date = new Date(s_date);
    console.log(s_date.getFullYear());
    var min_date = s_date
    switch (period) {
        case 'Yearly':
            min_date.setFullYear(s_date.getFullYear() + 1);
            min_date.setDate(min_date.getDate() - 1)
            min_date = formatDate(min_date)
            document.getElementById("end_date").setAttribute("min", min_date);
            console.log("Kuta");
            break;
        case 'Quarterly':
            min_date.setMonth(s_date.getMonth() + 3);
            min_date.setDate(min_date.getDate() - 1)
            min_date = formatDate(min_date)
            document.getElementById("end_date").setAttribute("min", min_date);
            console.log("Billi");
            break;
        case 'Monthly':
            min_date.setMonth(s_date.getMonth() + 1);
            min_date.setDate(min_date.getDate() - 1)
            min_date = formatDate(min_date)
            document.getElementById("end_date").setAttribute("min", min_date);
            console.log("Billi");
            break;
        case 'Bi-monthly':
            min_date.setMonth(s_date.getMonth() + 2);
            min_date.setDate(min_date.getDate() - 1)
            min_date = formatDate(min_date)
            document.getElementById("end_date").setAttribute("min", min_date);
            console.log("Billi");
            break;
        case 'Tri-annual':
            min_date.setMonth(s_date.getMonth() + 4);
            min_date.setDate(min_date.getDate() - 1)
            min_date = formatDate(min_date)
            document.getElementById("end_date").setAttribute("min", min_date);
            console.log("Billi");                    break;
        case 'Semi-annual':
            min_date.setMonth(s_date.getMonth() + 6);
            min_date.setDate(min_date.getDate() - 1)
            min_date = formatDate(min_date)
            document.getElementById("end_date").setAttribute("min", min_date);
            console.log("Billi");
    };
    document.getElementById("end_date").disabled = false;
};
console.log(s_date);