
define(['models/casestudy', 'views/data-entry/flows',
    'views/data-entry/actors', 'views/data-entry/materials',
    'views/data-entry/bulk-upload', 'collections/gdsecollection',
    'app-config', 'utils/utils', 'base'],
function (CaseStudy, FlowsView, ActorsView, EditMaterialsView, BulkUploadView,
    GDSECollection, appConfig, utils) {
    /**
    *
    * entry point for data-entry,
    * render tabs for entering data (edit actors, flows and materials)
    *
    * @author Christoph Franke
    * @module DataEntry
    */
    var _ = require('underscore');
    var caseStudy,
        keyflows,
        materials,
        activities,
        loader = new utils.Loader(document.getElementById('content'), {disable: true});

    var flowsView,
        actorsView,
        editMaterialsView,
        bulkUploadView;

    var refreshFlowsBtn = document.getElementById('refresh-flowview-btn'),
        refreshMaterialsBtn = document.getElementById('refresh-materialsview-btn'),
        refreshActorsBtn = document.getElementById('refresh-actorsview-btn');

    function renderFlows(keyflow){
        if (keyflow == null) return;
        if (flowsView != null)
            flowsView.close();
        flowsView = new FlowsView({
            el: document.getElementById('flows-content'),
            template: 'flows-edit-template',
            model: keyflow,
            materials: materials,
            activities: activities,
            caseStudy: caseStudy
        });
        refreshFlowsBtn.style.display = 'block';
    };

    function renderEditActors(keyflow){
        if (keyflow == null) return;
        if (actorsView != null)
            actorsView.close();
        // create casestudy-object and render view on it (data will be fetched in view)

        actorsView = new ActorsView({
            el: document.getElementById('actors-content'),
            template: 'actors-template',
            model: keyflow,
            caseStudy: caseStudy,
            activities: activities,
            onUpload: function(){renderEditActors(keyflow)}
        });
        refreshActorsBtn.style.display = 'block';
    };

    function renderBulkUpload(keyflow){
        if (keyflow == null) return;
        if (bulkUploadView != null)
            bulkUploadView.close();

        // create casestudy-object and render view on it (data will be fetched in view)

        bulkUploadView = new BulkUploadView({
            el: document.getElementById('bulk-upload'),
            template: 'bulk-upload-template',
            model: keyflow,
            caseStudy: caseStudy
        });
    }

    function renderEditMaterials(keyflow){
        if (keyflow == null) return;
        if (editMaterialsView != null)
            editMaterialsView.close();

        // create casestudy-object and render view on it (data will be fetched in view)

        editMaterialsView = new EditMaterialsView({
            el: document.getElementById('materials-content'),
            template: 'materials-edit-template',
            model: keyflow,
            caseStudy: caseStudy,
            materials: materials
        });
        refreshMaterialsBtn.style.display = 'block';
    };

    function createKeyflow(keyflowId){

        keyflows.create(
            { keyflow: keyflowId }, {
                success: function(){
                    document.querySelector('body').style.opacity=0.3;
                    location.reload();
                },
                error: function(res, t) { alert(t.responseText) }
            }
        )
    }

    function render(caseStudy){

        var keyflowSelect = document.getElementById('keyflow-select'),
            createKeyflowSelect = document.getElementById('create-keyflow-select'),
            createKeyflowModal = document.getElementById('create-keyflow-modal'),
            createBtn = createKeyflowModal.querySelector('.confirm');

        function getKeyflow(){
            return keyflows.get(keyflowSelect.value);
        }
        document.getElementById('keyflow-warning').style.display = 'block';
        keyflowSelect.addEventListener('change', function(){
            if (this.value === "new"){
                $(createKeyflowModal).modal('show');
                return;
            }
            var keyflow = getKeyflow();
            document.getElementById('keyflow-warning').style.display = 'none';
            materials = new GDSECollection([], {
                apiTag: 'materials',
                apiIds: [ caseStudy.id, keyflow.id ]
            });
            activities = new GDSECollection([], {
                apiTag: 'activities',
                apiIds: [ caseStudy.id, keyflow.id ]
            });
            loader.activate();
            Promise.all([materials.fetch(), activities.fetch()]).then(function(){
                loader.deactivate();
                renderFlows(keyflow);
                renderEditActors(keyflow);
                renderEditMaterials(keyflow);
                renderBulkUpload(keyflow);
            });
        });
        createBtn.addEventListener('click', function(){
            createKeyflow(createKeyflowSelect.value)
        });

        refreshFlowsBtn.addEventListener('click', function(){ renderFlows(getKeyflow()) });
        refreshMaterialsBtn.addEventListener('click', function(){ renderEditMaterials(getKeyflow()) });
        refreshActorsBtn.addEventListener('click', function(){ renderEditActors(getKeyflow()) });
        document.getElementById('keyflow-select').disabled = false;
    }

    appConfig.session.fetch({
        success: function(session){
            var caseStudyId = session.get('casestudy');
            if (caseStudyId == null){
                document.getElementById('keyflow-warning').style.display = 'none';
                return;
            }
            caseStudy = new CaseStudy({id: caseStudyId});
            keyflows = new GDSECollection([], {
                apiTag: 'keyflowsInCaseStudy',
                apiIds: [caseStudyId]
            });
            loader.activate();

            $.when(caseStudy.fetch(), keyflows.fetch()).then(function() {
                loader.deactivate();
                render(caseStudy);
            });
        }
    });
});
