/* globals Chart:false */

var manageJobss;
/* globals Chart:false */
$(document).ready(function() {  
  manageJobss =$('#managejobpostingsTable').DataTable({
      pageLength: 5, // Initial page length
      order: [[2, 'desc']],   // Sort by date by default
      language: {
          search: "",
          searchPlaceholder: 'Search jobs...',
          lengthMenu: "Show _MENU_entries",
          paginate: {
              first: '<i class="fa fa-angle-double-left"></i>',
              last: '<i class="fa fa-angle-double-right"></i>',
              next: '<i class="fa fa-angle-right"></i>',
              previous: '<i class="fa fa-angle-left"></i>'
          }
      },
      lengthMenu: [ [5, 10, 25, 50, -1], [5, 10, 25, 50, "All"] ], // Define the options for the length menu
      columnDefs: [
          { orderable: false, targets: 3 } // Disable sorting for actions column
      ],
      buttons: [
          {
              extend: 'csv',
              text: 'Export CSV',
              title: 'Csv Company Verification',
              className: 'btn btn-primary btn-sm',
                exportOptions: {
                  columns: [0, 1, 2] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              }
          },
          {
              extend: 'excel',
              text: 'Export Excel',
              title: 'Excel Company Verification',
              className: 'btn btn-success btn-sm',
              exportOptions: {
                  columns: [0, 1, 2] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              } 
          },
          {
              extend: 'pdf',
              text: 'Export PDF',
              title: 'Pdf Company Verification',
              className: 'btn btn-danger btn-sm',
              exportOptions: {
                  columns: [0, 1, 2] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              }
          },
          {
              extend: 'print',
              class: 'profile-buttons-print',
              title: 'Print Company Verification',
              exportOptions: {
                  columns: [0, 1, 2] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              }
          }
      ]
  });
});

$('#btn-excel').on('click', function(){
  manageJobss.button('.buttons-excel').trigger();
});
$('#btn-csv').on('click', function(){
  manageJobss.button('.buttons-csv').trigger();
});
$('#btn-pdf').on('click', function(){
  manageJobss.button('.buttons-pdf').trigger();
});
$('#btn-print').on('click', function(){
  manageJobss.button('.buttons-print').trigger();
});


var manageJobfair;
/* globals Chart:false */
$(document).ready(function() {  
  manageJobfair = $('#managejobFairpostingsTable').DataTable({
      pageLength: 5, // Initial page length
      order: [[2, 'desc']],   // Sort by date by default
      language: {
          search: "",
          searchPlaceholder: 'Search job fairs...',
          lengthMenu: "Show _MENU_entries",
          paginate: {
              first: '<i class="fa fa-angle-double-left"></i>',
              last: '<i class="fa fa-angle-double-right"></i>',
              next: '<i class="fa fa-angle-right"></i>',
              previous: '<i class="fa fa-angle-left"></i>'
          }
      },
      lengthMenu: [ [5, 10, 25, 50, -1], [5, 10, 25, 50, "All"] ], // Define the options for the length menu
      columnDefs: [
          { orderable: false, targets: 3 } // Disable sorting for actions column
      ],
      buttons: [
          {
              extend: 'csv',
              text: 'Export CSV',
              title: 'Csv Company Verification',
              className: 'btn btn-primary btn-sm',
                exportOptions: {
                  columns: [0, 1, 2] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              }
          },
          {
              extend: 'excel',
              text: 'Export Excel',
              title: 'Excel Company Verification',
              className: 'btn btn-success btn-sm',
              exportOptions: {
                  columns: [0, 1, 2] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              } 
          },
          {
              extend: 'pdf',
              text: 'Export PDF',
              title: 'Pdf Company Verification',
              className: 'btn btn-danger btn-sm',
              exportOptions: {
                  columns: [0, 1, 2] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              }
          },
          {
              extend: 'print',
              class: 'profile-buttons-print',
              title: 'Print Company Verification',
              exportOptions: {
                  columns: [0, 1, 2] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              }
          }
      ]
  });
});

$('#btn-excel').on('click', function(){
  manageJobfair.button('.buttons-excel').trigger();
});
$('#btn-csv').on('click', function(){
  manageJobfair.button('.buttons-csv').trigger();
});
$('#btn-pdf').on('click', function(){
  manageJobfair.button('.buttons-pdf').trigger();
});
$('#btn-print').on('click', function(){
  manageJobfair.button('.buttons-print').trigger();
});

var companyVerify;
/* globals Chart:false */
/* globals Chart:false */
$(document).ready(function() {  
  companyVerify =$('#companyverifiedTable').DataTable({
      pageLength: 5, // Initial page length
      order: [[2, 'desc']],   // Sort by date by default
      language: {
          search: "",
          searchPlaceholder: 'Search jobs...',
          lengthMenu: "Show _MENU_entries",
          paginate: {
              first: '<i class="fa fa-angle-double-left"></i>',
              last: '<i class="fa fa-angle-double-right"></i>',
              next: '<i class="fa fa-angle-right"></i>',
              previous: '<i class="fa fa-angle-left"></i>'
          }
      },
      lengthMenu: [ [5, 10, 25, 50, -1], [5, 10, 25, 50, "All"] ], // Define the options for the length menu
      columnDefs: [
          { orderable: false, targets: 3 } // Disable sorting for actions column
      ],
      buttons: [
          {
              extend: 'csv',
              text: 'Export CSV',
              title: 'Csv Company Verification',
              className: 'btn btn-primary btn-sm',
                exportOptions: {
                  columns: [0, 1, 2] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              }
          },
          {
              extend: 'excel',
              text: 'Export Excel',
              title: 'Excel Company Verification',
              className: 'btn btn-success btn-sm',
              exportOptions: {
                  columns: [0, 1, 2] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              } 
          },
          {
              extend: 'pdf',
              text: 'Export PDF',
              title: 'Pdf Company Verification',
              className: 'btn btn-danger btn-sm',
              exportOptions: {
                  columns: [0, 1, 2] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              }
          },
          {
              extend: 'print',
              class: 'profile-buttons-print',
              title: 'Print Company Verification',
              exportOptions: {
                  columns: [0, 1, 2] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              }
          }
      ]
  });
});

$('#btn-excel').on('click', function(){
  companyVerify.button('.buttons-excel').trigger();
});
$('#btn-csv').on('click', function(){
  companyVerify.button('.buttons-csv').trigger();
});
$('#btn-pdf').on('click', function(){
  companyVerify.button('.buttons-pdf').trigger();
});
$('#btn-print').on('click', function(){
  companyVerify.button('.buttons-print').trigger();
});


var manageEmployer;
/* globals Chart:false */
$(document).ready(function() {  
  manageEmployer =$('#manageEmployerTable').DataTable({
      pageLength: 5, 
      language: {
          search: "",
          searchPlaceholder: 'Search Employer...',
          lengthMenu: "Show _MENU_entries",
          paginate: {
              first: '<i class="fa fa-angle-double-left"></i>',
              last: '<i class="fa fa-angle-double-right"></i>',
              next: '<i class="fa fa-angle-right"></i>',
              previous: '<i class="fa fa-angle-left"></i>'
          }
      },
      lengthMenu: [ [5, 10, 25, 50, -1], [5, 10, 25, 50, "All"] ], // Define the options for the length menu
      columnDefs: [
          { orderable: false, targets: 2 } // Disable sorting for actions column
      ],
      buttons: [
          {
              extend: 'csv',
              text: 'Export CSV',
              title: 'Csv Company Verification',
              className: 'btn btn-primary btn-sm',
                exportOptions: {
                  columns: [0, 1, 2] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              }
          },
          {
              extend: 'excel',
              text: 'Export Excel',
              title: 'Excel Company Verification',
              className: 'btn btn-success btn-sm',
              exportOptions: {
                  columns: [0, 1, 2] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              } 
          },
          {
              extend: 'pdf',
              text: 'Export PDF',
              title: 'Pdf Company Verification',
              className: 'btn btn-danger btn-sm',
              exportOptions: {
                  columns: [0, 1, 2] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              }
          },
          {
              extend: 'print',
              class: 'profile-buttons-print',
              title: 'Print Company Verification',
              exportOptions: {
                  columns: [0, 1, 2] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              }
          }
      ]
  });
});

$('#btn-excel').on('click', function(){
  manageEmployer.button('.buttons-excel').trigger();
});
$('#btn-csv').on('click', function(){
  manageEmployer.button('.buttons-csv').trigger();
});
$('#btn-pdf').on('click', function(){
  manageEmployer.button('.buttons-pdf').trigger();
});
$('#btn-print').on('click', function(){
  manageEmployer.button('.buttons-print').trigger();
});


var manageApplicant;
/* globals Chart:false */
$(document).ready(function() {  
  manageApplicant =$('#manageApplicantTable').DataTable({
      pageLength: 5, // Initial page length
      language: {
          search: "",
          searchPlaceholder: 'Search Applicant...',
          lengthMenu: "Show _MENU_entries",
          paginate: {
              first: '<i class="fa fa-angle-double-left"></i>',
              last: '<i class="fa fa-angle-double-right"></i>',
              next: '<i class="fa fa-angle-right"></i>',
              previous: '<i class="fa fa-angle-left"></i>'
          }
      },
      lengthMenu: [ [5, 10, 25, 50, -1], [5, 10, 25, 50, "All"] ], // Define the options for the length menu
      columnDefs: [
          { orderable: false, targets: 2 } // Disable sorting for actions column
      ],
      buttons: [
          {
              extend: 'csv',
              text: 'Export CSV',
              title: 'Csv Company Verification',
              className: 'btn btn-primary btn-sm',
                exportOptions: {
                  columns: [0, 1] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              }
          },
          {
              extend: 'excel',
              text: 'Export Excel',
              title: 'Excel Company Verification',
              className: 'btn btn-success btn-sm',
              exportOptions: {
                  columns: [0, 1] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              } 
          },
          {
              extend: 'pdf',
              text: 'Export PDF',
              title: 'Pdf Company Verification',
              className: 'btn btn-danger btn-sm',
              exportOptions: {
                  columns: [0, 1] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              }
          },
          {
              extend: 'print',
              class: 'profile-buttons-print',
              title: 'Print Company Verification',
              exportOptions: {
                  columns: [0, 1] // Exclude the last column
              },
              init: function (api, node, config){
                  $(node).hide();
              }
          }
      ]
  });
});

$('#btn-excel').on('click', function(){
  manageApplicant.button('.buttons-excel').trigger();
});
$('#btn-csv').on('click', function(){
  manageApplicant.button('.buttons-csv').trigger();
});
$('#btn-pdf').on('click', function(){
  manageApplicant.button('.buttons-pdf').trigger();
});
$('#btn-print').on('click', function(){
  manageApplicant.button('.buttons-print').trigger();
});
