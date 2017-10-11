require(['./libs/domReady!', './app'], function (doc, app) {
    requirejs(['app/admin-data-tree']);

    document.getElementById('balance-verify-button-group').style.display = 'none';
    document.getElementById('balance-verify-single').style.display = 'none';
    document.getElementById('data-tree-group').style.display = 'none';

    var deactivateTabs = function(){
        var tabs = document.querySelectorAll('.admin-tab');
        console.log(tabs);
        tabs.forEach(function(tab) {
            tab.classList.remove('active');
        });
    }
    
    document.getElementById('enter-data-btn').addEventListener(
        'click', function(){
            deactivateTabs();
            var tab =  document.getElementById('activity-groups-edit');
            tab.classList.add('active');
            document.getElementById('data-tree-group').style.display = 'block';
        });

    document.getElementById('view-data-btn').addEventListener(
        'click', function(){
            deactivateTabs();
            var tab =  document.getElementById('sankey');
            tab.classList.add('active');
            document.getElementById('data-tree-group').style.display = 'none';
        });

});