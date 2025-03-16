var jobPostings;

$(document).ready(function() {
    if (!$.fn.DataTable.isDataTable('#jobPostingsTable')) {
        jobPostings = $('#jobPostingsTable').DataTable({
            pageLength: 5, // Initial page length
            order: [[4, 'desc']], // Sort by date by default
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
            lengthMenu: [ [5, 10, 25, 50, -1], [5, 10, 25, 50, "All"] ],
            columnDefs: [
                { orderable: false, targets: [1, 2, 3, 5] } // Disable sorting for specific columns
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
                    init: function (api, node, config) {
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
                    init: function (api, node, config) {
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
                    init: function (api, node, config) {
                        $(node).hide();
                    }
                }
            ]
        });
    }
});

// Export button triggers
$('#btn-excel').on('click', function() {
    jobPostings.button('.buttons-excel').trigger();
});
$('#btn-csv').on('click', function() {
    jobPostings.button('.buttons-csv').trigger();
});
$('#btn-print').on('click', function() {
    jobPostings.button('.buttons-print').trigger();
});

var jobApplication;

$(document).ready(function() {
    if (!$.fn.DataTable.isDataTable('#jobApplicationStatusTable')) {
        jobApplication = $('#jobApplicationStatusTable').DataTable({
            pageLength: 5, // Initial page length
            order: [[2,'asc']],   // Sort by date by default
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
    }
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

var jobfairPostings;

$(document).ready(function() {
    if (!$.fn.DataTable.isDataTable('#jobfairPostingsTable')) {
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
    }
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
    if (!$.fn.DataTable.isDataTable('#applicationAnalyticsTable')) {
        applicationAnalytics = $('#applicationAnalyticsTable').DataTable({
            pageLength: 3, // Initial page length
            order: [[2, 'asc']],   // Sort by date by default
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
    }
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
    if (!$.fn.DataTable.isDataTable('#jobAnalyticsTable')) {
        jobAnalytics = $('#jobAnalyticsTable').DataTable({
            pageLength: 3, // Initial page length
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
            lengthMenu: [ [3, 5, 10, 25, 50, -1], [3, 5, 10, 25, 50, "All"] ], // Define the options for the length menu
            columnDefs: [
                { orderable: false, targets: [1,2,3,5] } // Disable sorting for actions column
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
    }
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
    if (!$.fn.DataTable.isDataTable('#jobFairTable')) {
        jobFairRegis = $('#jobFairTable').DataTable({
            pageLength: 5, // Initial page length
            order: [[2, 'asc']],   // Sort by date by default
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
    }
});

$(document).ready(function() {
    if (!$.fn.DataTable.isDataTable('#jobSavedTable')) {
        $('#jobSavedTable').DataTable({
            pageLength: 5, // Initial page length
            order: [[2, 'asc']],   // Sort by date by default
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
    }
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

function showJobDetails(element) {
    // Get job ID from the data attribute
    const jobId = element.getAttribute("data-id");

    // Remove 'active' class from all job cards and job details
    document.querySelectorAll('.job-card').forEach(card => {
        card.classList.remove('active');
    });
    document.querySelectorAll('.job-details').forEach(detail => {
        detail.classList.remove('active');
    });

    // Add 'active' class to the clicked job card and show corresponding job details
    element.classList.add('active');
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

   
    document.querySelector(`.inbox-card[onclick="showInboxDetails(${inboxId})"]`).classList.add('active');
    const activeInboxDetail = document.getElementById(`inbox-${inboxId}`);
    activeInboxDetail.classList.add('active');

    const messagesContainer = activeInboxDetail.querySelector('.messages-container');
    if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
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
    
    // Log validation success for debugging
    console.log(`Step ${step} validation successful`);
    
    // If we're on step 1 and about to go to step 2, save the fact that we validated
    if (step == 1) {
        console.log("Step 1 complete - ready to show phone input");
        // We can add any preparation needed for step 2 here
    }
    
    return true;
}

// Add these functions to work with your existing navigation code
function monitorPhoneCountry() {
    // Check if intlTelInput is initialized
    if (typeof iti !== 'undefined') {
        // Get the currently selected country
        const currentCountry = iti.getSelectedCountryData();
        console.log("Current phone country:", currentCountry.name);
        console.log("Country code:", currentCountry.dialCode);
        
        // Store in console session for test debugging
        console.log("Stored country ISO:", currentCountry.iso2);
        return currentCountry.iso2;
    } else {
        console.log("Phone input not yet initialized");
        return null;
    }
}

// Function to test navigation between steps
function testPhoneCountryPersistence() {
    // Current step
    const currentStep = document.getElementById('currentStep').value;
    console.log("Current step:", currentStep);
    
    if (currentStep == "1") {
        // Go to step 2
        console.log("Testing navigation to step 2...");
        nextStep(2);
        
        // After a brief delay, check the phone country
        setTimeout(() => {
            console.log("After navigation to step 2:");
            monitorPhoneCountry();
            
            // Change country (for testing)
            if (typeof iti !== 'undefined') {
                console.log("Changing country to Germany for test...");
                iti.setCountry('de');
                monitorPhoneCountry();
                
                // Go back to step 1
                console.log("Going back to step 1...");
                prevStep(1);
                
                // Then go back to step 2 to check if country persists
                setTimeout(() => {
                    console.log("Going back to step 2 to check persistence...");
                    nextStep(2);
                    
                    // Check if country persisted
                    setTimeout(() => {
                        console.log("Country after round trip:");
                        monitorPhoneCountry();
                    }, 300);
                }, 700);
            }
        }, 500);
    } else {
        // If on step 2, monitor current country
        monitorPhoneCountry();
        
        // Go to step 1
        console.log("Testing navigation to step 1...");
        prevStep(1);
        
        // Go back to step 2
        setTimeout(() => {
            console.log("Going back to step 2...");
            nextStep(2);
            
            // Check if country persisted
            setTimeout(() => {
                console.log("Country after navigation:");
                monitorPhoneCountry();
            }, 300);
        }, 700);
    }
}

// GO TO FIND JOBS Homepage
document.getElementById("findjobs-link").addEventListener("click", function(event) {
    event.preventDefault(); // Prevent the default anchor click behavior
    const findJobsSection = document.getElementById("findjobs");
    
    // Adjust the scroll position with a smooth scroll effect
    window.scrollTo({
        top: findJobsSection.offsetTop - 150, // Adjust based on the navbar height
        behavior: 'smooth'
    });
});