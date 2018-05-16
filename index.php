<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="favicon.png" rel="shortcut icon" type="image/png"/>
    <title>PJATK - Plan zajęć z wyszukiwarką</title>
    <link href="//cdn.datatables.net/1.10.16/css/jquery.dataTables.min.css" rel="stylesheet" type="text/css"/>
    <script src="https://code.jquery.com/jquery-2.2.4.min.js"
            integrity="sha256-BbhdlvQf/xTY9gja0Dq3HiwQF8LaCRTXxZKRutelT44="
            crossorigin="anonymous"></script>
    <script src="//cdn.datatables.net/1.10.16/js/jquery.dataTables.min.js" type="text/javascript"></script>
    <style>
        .nowrap {
            white-space: nowrap;
        }
    </style>
</head>
<body class="">
<h3>
    Plan zajęć PJATK
    <small>(Polsko-Japońska Akademia Technik Komputerowych - dawniej PJWSTK)</small>
    z wyszukiwarką
</h3>

<h4>Załadowany zakres dat od <span id="startDate"></span> do <span id="endDate"></span>,
    <span style="color:red">wyszukiwarka po prawej stronie &#8680;</span>
</h4>

<small>Skrypt do pobrania z <a href="https://github.com/JSkalskiSBG/PJATK-schedule-crawler">https://github.com/JSkalskiSBG/PJATK-schedule-crawler</a></small>

<table id="schedule" class="display" width="100%"></table>

<script>
    let dataSet = <?php echo file_get_contents('crawler/data.json'); ?>;

    let startDate = dataSet[0][0];
    let endDate = dataSet[dataSet.length - 1][0];

    function onlyUniqueFilter(value, index, self) {
        return self.indexOf(value) === index;
    }

    $(document).ready(function () {
        $('#startDate').text(startDate);
        $('#endDate').text(endDate);

        let scheduleTable = $('#schedule').DataTable({
            data: dataSet,
            pagingType: 'full_numbers',
            pageLength: 100,
            lengthMenu: [100, 500],
            order: [[0, 'asc'], [1, 'asc']],
            columns: [
                {
                    title: 'Czas', data: null, className: 'nowrap', render: function (data, type, row) {
                        return data[0] + ', ' + data[1] + ' - ' + data[2];
                    }
                },
                {
                    title: 'Budynek i Sala', data: null, render: function (data, type, row) {
                        return data[3] + ' - ' + data[4];
                    }
                },
                {
                    title: 'Prowadzący', data: null, render: function (data, type, row) {
                        return data[5].split(', ').filter(onlyUniqueFilter).join(', ');
                    }
                },
                {
                    title: 'Przedmiot', data: null, render: function (data, type, row) {
                        return data[6] + ' - ' + data[7] + ' - ' + data[8];
                    }
                },
                {
                    title: 'Osoby', data: null, render: function (data, type, row) {
                        return data[9] + ' - ' + data[10];
                    }
                }
            ]
        });
    });</script>
</body>
</html>