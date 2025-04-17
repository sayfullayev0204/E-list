$(document).ready(function() {
    // Toggle sidebar on button click
    $('#sidebarCollapse, #sidebarCollapseDesktop').on('click', function() {
        $('#sidebar').toggleClass('active');
        $('#content').toggleClass('active');
    });

    // Ensure sidebar is visible on desktop by default
    if ($(window).width() >= 768) {
        $('#sidebar').removeClass('active');
        $('#content').removeClass('active');
    }

    // Handle window resize to reset sidebar state
    $(window).resize(function() {
        if ($(window).width() >= 768) {
            $('#sidebar').removeClass('active');
            $('#content').removeClass('active');
        } else {
            $('#sidebar').addClass('active');
            $('#content').removeClass('active');
        }
    });
});