define(['d3', 'models/casestudy', 'visualizations/sankey-map',
    'views/study-area/maps', 'views/study-area/setup-maps', 
    'views/study-area/charts',
    'views/study-area/stakeholders',
    'app-config', 'base',
    'static/css/study-area.css'
], function(d3, CaseStudy, SankeyMap, BaseMapsView, SetupMapsView, BaseChartsView, 
    StakeholdersView, appConfig) {

    function renderWorkshop(caseStudy){
        var mapsView = new BaseMapsView({
            template: 'base-maps-template',
            el: document.getElementById('base-map-content'),
            caseStudy: caseStudy
        });
        var chartsView = new BaseChartsView({
            template: 'base-charts-template',
            el: document.getElementById('base-charts-content'),
            caseStudy: caseStudy
        });
        var stakeholdersView = new StakeholdersView({
            template: 'stakeholders-template',
            el: document.getElementById('stakeholders-content'),
            caseStudy: caseStudy
        });
    }
    
    function renderSetup(caseStudy){
        var mapsView = new SetupMapsView({
            template: 'setup-maps-template',
            el: document.getElementById('base-map-content'),
            caseStudy: caseStudy
        });
        var chartsView = new BaseChartsView({
            template: 'base-charts-template',
            el: document.getElementById('base-charts-content'),
            caseStudy: caseStudy,
            mode: 1
        });
        var stakeholdersView = new StakeholdersView({
            template: 'stakeholders-template',
            el: document.getElementById('stakeholders-content'),
            caseStudy: caseStudy,
            mode: 1
        });
    }
    
    appConfig.session.fetch({
        success: function(session){
            var mode = session.get('mode'),
                caseStudyId = session.get('casestudy'),
                caseStudy = new CaseStudy({id: caseStudyId});
    
            caseStudy.fetch({success: function(){
                if (Number(mode) == 1) {
                    renderSetup(caseStudy);
                }
                else {
                    renderWorkshop(caseStudy);
                }
            }});
        }
    });

});