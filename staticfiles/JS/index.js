var jobPostings;

$(document).ready(function() {
    jobPostings = $('#jobPostingsTable').DataTable({
        pageLength: 5, // Initial page length
        order: [[4, 'desc']],   // Sort by date by default
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
            { orderable: false, targets: 5 } // Disable sorting for actions column
        ],
        buttons: [
            {
                extend: 'csv',
                text: 'Export CSV',
                title: 'Csv Employer Manage Jobs',
                className: 'btn btn-primary btn-sm',
                  exportOptions: {
                    columns: [0, 1, 2, 4] // Exclude the last column
                },
                init: function (api, node, config){
                    $(node).hide();
                }
            },
            {
                extend: 'excel',
                text: 'Export Excel',
                title: 'Excel Employer Manage Jobs',
                className: 'btn btn-success btn-sm',
                exportOptions: {
                    columns: [0, 1, 2, 4] // Exclude the last column
                },
                init: function (api, node, config){
                    $(node).hide();
                } 
            },
            {
                extend: 'print',
                class: 'profile-buttons-print',
                title: 'Print Employer Manage Jobs',
                exportOptions: {
                    columns: [0, 1, 2, 4] // Exclude the last column
                },
                init: function (api, node, config){
                    $(node).hide();
                }
            }
        ]
    });
});

$('#btn-excel').on('click', function(){
    jobPostings.button('.buttons-excel').trigger();
  });
$('#btn-csv').on('click', function(){
    jobPostings.button('.buttons-csv').trigger();
});
$('#btn-print').on('click', function(){
    jobPostings.button('.buttons-print').trigger();
});
  
var jobApplication;

$(document).ready(function() {
    jobApplication = $('#jobApplicationStatusTable').DataTable({
        pageLength: 5, // Initial page length
        order: [[2,'desc']],   // Sort by date by default
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
            { orderable: false, targets: 4 } // Disable sorting for actions column
        ],
        buttons: [
            {
                extend: 'csv',
                text: 'Export CSV',
                title: 'Csv Applicant Job Applications',
                className: 'btn btn-primary btn-sm',
                  exportOptions: {
                    columns: [0, 1, 2, 4] // Exclude the last column
                },
                init: function (api, node, config){
                    $(node).hide();
                }
            },
            {
                extend: 'excel',
                text: 'Export Excel',
                title: 'Excel Applicant Job Applications',
                className: 'btn btn-success btn-sm',
                exportOptions: {
                    columns: [0, 1, 2, 4] // Exclude the last column
                },
                init: function (api, node, config){
                    $(node).hide();
                } 
            },
            {
                extend: 'print',
                class: 'profile-buttons-print',
                title: 'Print Applicant Job Applications',
                exportOptions: {
                    columns: [0, 1, 2, 4] // Exclude the last column
                },
                init: function (api, node, config){
                    $(node).hide();
                }
            }
        ]
    });
});

$('#btn-excel').on('click', function(){
    jobApplication.button('.buttons-excel').trigger();
  });
$('#btn-csv').on('click', function(){
    jobApplication.button('.buttons-csv').trigger();
});
$('#btn-print').on('click', function(){
    jobApplication.button('.buttons-print').trigger();
});


$(document).ready(function() {
    jobRegistration = $('#jobfairregistersStatusTable').DataTable({
        pageLength: 5, // Initial page length
        order: [[2,'asc']],   // Sort by date by default
        language: {
            search: "",
            searchPlaceholder: 'Search applicant job fair...',
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
        ]
    });
});


var jobfairPostings;

$(document).ready(function() {
    jobfairPostings = $('#jobfairPostingsTable').DataTable({
        pageLength: 5, // Initial page length
        order: [[4, 'desc']],   // Sort by date by default
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
            { orderable: false, targets: 5 } // Disable sorting for actions column
        ],
        buttons: [
            {
                extend: 'csv',
                text: 'Export CSV',
                title: 'Csv Employer Manage Job Fair',
                className: 'btn btn-primary btn-sm',
                  exportOptions: {
                    columns: [0, 1, 2, 4] // Exclude the last column
                },
                init: function (api, node, config){
                    $(node).hide();
                }
            },
            {
                extend: 'excel',
                text: 'Export Excel',
                title: 'Excel Employer Manage Job Fair',
                className: 'btn btn-success btn-sm',
                exportOptions: {
                    columns: [0, 1, 2, 4] // Exclude the last column
                },
                init: function (api, node, config){
                    $(node).hide();
                } 
            },
            {
                extend: 'print',
                class: 'profile-buttons-print',
                title: 'Print Employer Manage Job Fair',
                exportOptions: {
                    columns: [0, 1, 2, 4] // Exclude the last column
                },
                init: function (api, node, config){
                    $(node).hide();
                }
            }
        ]
    });
});

$('#btn-excel').on('click', function(){
    jobfairPostings.button('.buttons-excel').trigger();
  });
$('#btn-csv').on('click', function(){
    jobfairPostings.button('.buttons-csv').trigger();
});
$('#btn-print').on('click', function(){
    jobfairPostings.button('.buttons-print').trigger();
});

var applicationAnalytics;

$(document).ready(function() {
    applicationAnalytics = $('#applicationAnalyticsTable').DataTable({
        pageLength: 3, // Initial page length
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
        lengthMenu: [ [3, 5, 10, 25, 50, -1], [3, 5, 10, 25, 50, "All"] ], // Define the options for the length menu
        columnDefs: [
            { orderable: false, targets: 3 } // Disable sorting for actions column
        ],
        buttons: [
            {
                extend: 'csv',
                text: 'Export CSV',
                title: 'Csv Employer Manage Jobs',
                className: 'btn btn-primary btn-sm',
                  exportOptions: {
                    columns: [0, 1, 2, 4] // Exclude the last column
                },
                init: function (api, node, config){
                    $(node).hide();
                } 
            },
            {
                extend: 'excel',
                text: 'Export Excel',
                title: 'Excel Employer Manage Jobs',
                className: 'btn btn-success btn-sm',
                exportOptions: {
                    columns: [0, 1, 2, 4] // Exclude the last column
                },
                init: function (api, node, config){
                    $(node).hide();
                } 
            },
            {
                extend: 'print',
                class: 'profile-buttons-print',
                title: 'Print Employer Manage Jobs',
                exportOptions: {
                    columns: [0, 1, 2, 4] // Exclude the last column
                },
                init: function (api, node, config){
                    $(node).hide();
                }
            }
        ]
    });
});


$('#btn-excel').on('click', function(){
    applicationAnalytics.button('.buttons-excel').trigger();
  });
$('#btn-csv').on('click', function(){
    applicationAnalytics.button('.buttons-csv').trigger();
});
$('#btn-print').on('click', function(){
    applicationAnalytics.button('.buttons-print').trigger();
});


var jobAnalytics;

$(document).ready(function() {
    jobAnalytics = $('#jobAnalyticsTable').DataTable({
        pageLength: 3, // Initial page length
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
        lengthMenu: [ [3, 5, 10, 25, 50, -1], [3, 5, 10, 25, 50, "All"] ], // Define the options for the length menu
        columnDefs: [
            { orderable: false, targets: 3 } // Disable sorting for actions column
        ],
        buttons: [
            {
                extend: 'csv',
                text: 'Export CSV',
                title: 'Csv Employer Manage Applications',
                className: 'btn btn-primary btn-sm',
                  exportOptions: {
                    columns: [0, 1, 2, 4] // Exclude the last column
                },
                init: function (api, node, config){
                    $(node).hide();
                }
            },
            {
                extend: 'excel',
                text: 'Export Excel',
                title: 'Excel Employer Manage Applications',
                className: 'btn btn-success btn-sm',
                exportOptions: {
                    columns: [0, 1, 2, 4] // Exclude the last column
                },
                init: function (api, node, config){
                    $(node).hide();
                } 
            },
            {
                extend: 'print',
                class: 'profile-buttons-print',
                title: 'Print Employer Manage Applications',
                exportOptions: {
                    columns: [0, 1, 2, 4] // Exclude the last column
                },
                init: function (api, node, config){
                    $(node).hide();
                }
            }
        ]

    });
});

$('#btn-excel').on('click', function(){
    jobAnalytics.button('.buttons-excel').trigger();
  });
$('#btn-csv').on('click', function(){
    jobAnalytics.button('.buttons-csv').trigger();
});
$('#btn-print').on('click', function(){
    jobAnalytics.button('.buttons-print').trigger();
});

var jobFairRegis;

$(document).ready(function() {
    jobFairRegis = $('#jobFairTable').DataTable({
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
                title: 'Csv Employer Manage Jobs',
                className: 'btn btn-primary btn-sm',
                  exportOptions: {
                    columns: [0, 1, 2, 4] // Exclude the last column
                },
                init: function (api, node, config){
                    $(node).hide();
                }
            },
            {
                extend: 'excel',
                text: 'Export Excel',
                title: 'Excel Employer Manage Jobs',
                className: 'btn btn-success btn-sm',
                exportOptions: {
                    columns: [0, 1, 2, 4] // Exclude the last column
                },
                init: function (api, node, config){
                    $(node).hide();
                } 
            },
            {
                extend: 'print',
                class: 'profile-buttons-print',
                title: 'Print Employer Manage Jobs',
                exportOptions: {
                    columns: [0, 1, 2, 4] // Exclude the last column
                },
                init: function (api, node, config){
                    $(node).hide();
                }
            }
        ]
    });
});

$(document).ready(function() {
    $('#jobSavedTable').DataTable({
        pageLength: 5, // Initial page length
        order: [[2, 'desc']],   // Sort by date by default
        language: {
            search: "",
            searchPlaceholder: 'Search saved job...',
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
        ]
    });
});

// ============== Scroll to Top ================ //
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
    }

    window.addEventListener('scroll', function() {
    var scrollButton = document.getElementById('scroll-to-top');
    if (window.scrollY > 300) {
        scrollButton.style.display = 'block';
    } else {
        scrollButton.style.display = 'none';
    }
});
  
// ============== End of Scroll to Top ================ //

// END OF GO TO FIND JOBS Homepage

document.getElementById("filter-btn").addEventListener("click", function() {
    const filterOptions = document.getElementById("filter-options");
    const mainHeading = document.getElementById("main-heading");
    const subHeading = document.getElementById("sub-heading");
    
    filterOptions.classList.toggle("filter-hidden");
    filterOptions.classList.toggle("filter-visible");

    mainHeading.classList.toggle("d-none");
    subHeading.classList.toggle("d-none");
});

function showJobDetails(jobId) {
    // Remove 'active' class from all job cards and hide all job details
    document.querySelectorAll('.job-card').forEach(card => {
        card.classList.remove('active');
    });
    document.querySelectorAll('.job-details').forEach(detail => {
        detail.classList.remove('active');
    });

    // Add 'active' class to the clicked job card and display corresponding job details
    document.querySelector(`.job-card[onclick="showJobDetails(${jobId})"]`).classList.add('active');
    document.getElementById(`job-${jobId}`).classList.add('active');
}

function showInboxDetails(inboxId) {
    // Remove 'active' class from all job cards and hide all job details
    document.querySelectorAll('.inbox-card').forEach(card => {
        card.classList.remove('active');
    });
    document.querySelectorAll('.inbox-details').forEach(detail => {
        detail.classList.remove('active');
    });

    // Add 'active' class to the clicked inbox card and display corresponding inbox details
    document.querySelector(`.inbox-card[onclick="showInboxDetails(${inboxId})"]`).classList.add('active');
    const activeInboxDetail = document.getElementById(`inbox-${inboxId}`);
    activeInboxDetail.classList.add('active');

    // Scroll to the bottom of the messages container
    const messagesContainer = activeInboxDetail.querySelector('.messages-container');
    if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}


// JavaScript to manage the step flow
let currentStep = 1;

function nextStep(step) {
    if (validateStep(step)) {
        // Hide current step
        document.getElementById('step' + step).classList.add('d-none');
        // Show next step
        document.getElementById('step' + (step + 1)).classList.remove('d-none');
        currentStep = step + 1;

        // Show the navigation buttons once we're past step 1
        if (currentStep > 1) {
            document.getElementById('navigationButtons').classList.remove('d-none');
        }
    }
}

function previousStep() {
    // Hide current step
    document.getElementById('step' + currentStep).classList.add('d-none');
    // Show previous step
    document.getElementById('step' + (currentStep - 1)).classList.remove('d-none');
    currentStep -= 1;

    // Hide the "Previous" button if we're on the first step
    if (currentStep === 1) {
        document.getElementById('navigationButtons').classList.add('d-none');
    }
}

function validateStep(step) {
    // Simple validation for required fields
    const inputs = document.querySelectorAll(`#step${step} input`);
    for (let input of inputs) {
        if (!input.checkValidity()) {
            input.reportValidity();
            return false;
        }
    }
    return true;
}
