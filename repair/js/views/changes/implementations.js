define(['views/baseview', 'backbone', 'underscore', 'collections/stakeholders',
        'collections/stakeholdercategories', 'collections/solutioncategories',
        'collections/solutions', 'visualizations/map', 
        'app-config', 'utils/loader', 'utils/utils', 'openlayers', 'bootstrap', 'bootstrap-select'],

function(BaseView, Backbone, _, Stakeholders, StakeholderCategories, 
         SolutionCategories, Solutions, Map, config, Loader, utils, ol){
/**
*
* @author Christoph Franke
* @name module:views/ImplementationsView
* @augments BaseView
*/
var ImplementationsView = BaseView.extend(
    /** @lends module:views/ImplementationsView.prototype */
    {

    /**
    * render workshop view on implementations
    *
    * @param {Object} options
    * @param {HTMLElement} options.el                          element the view will be rendered in
    * @param {string} options.template                         id of the script element containing the underscore template to render this view
    * @param {module:models/CaseStudy} options.caseStudy       the casestudy to add implementations to
    *
    * @constructs
    * @see http://backbonejs.org/#View
    */
    initialize: function(options){
        ImplementationsView.__super__.initialize.apply(this, [options]);
        _.bindAll(this, 'renderImplementation');
        _.bindAll(this, 'renderSolution');
        var _this = this;
        this.caseStudy = options.caseStudy;
        this.stakeholderCategories = new StakeholderCategories([], { caseStudyId: this.caseStudy.id });
        var Implementations = Backbone.Collection.extend({ url: config.api.implementations.format(this.caseStudy.id) });
        this.implementations = new Implementations();
        this.solutionCategories = new SolutionCategories([], { caseStudyId: this.caseStudy.id });
        this.stakeholders = [];
        this.solutions = [];
        this.projection = 'EPSG:4326';
        var Units = Backbone.Collection.extend({ url: config.api.units });
        this.units = new Units();
        $.when(this.implementations.fetch(), this.stakeholderCategories.fetch(), 
               this.solutionCategories.fetch(), this.units.fetch()).then(function(){
            var deferreds = [];
            _this.stakeholderCategories.forEach(function(category){
                var stakeholders = new Stakeholders([], { 
                    caseStudyId: _this.caseStudy.id, 
                    stakeholderCategoryId: category.id 
                });
                category.stakeholders = stakeholders;
                deferreds.push(stakeholders.fetch({ error: _this.onError }))
            });
            _this.solutionCategories.forEach(function(category){
                var solutions = new Solutions([], { 
                    caseStudyId: _this.caseStudy.id, 
                    solutionCategoryId: category.id 
                });
                category.solutions = solutions;
                deferreds.push(solutions.fetch({ error: _this.onError }))
            });
            
            $.when.apply($, deferreds).then(function(){
                _this.render();
            });
               
        })
    },
     
    /*
    * dom events (managed by jquery)
    */
    events: {
        'click #add-implementation': 'addImplementation',
    },

    /*
    * render the view
    */
    render: function(){
        
        var html = document.getElementById(this.template).innerHTML,
            template = _.template(html),
            _this = this;
        this.el.innerHTML = template({ 
            stakeholderCategories: this.stakeholderCategories,
            solutionCategories: this.solutionCategories
        });
        $('#coordinator-select').selectpicker();
        $('#solution-select').selectpicker();
        
        this.implementations.forEach(this.renderImplementation);
        
        document.querySelector('#implementation-modal .confirm').addEventListener('click', function(){ _this.confirmImplementation() })
        document.querySelector('#add-solution-modal .confirm').addEventListener('click', function(){ _this.confirmNewSolution() })
    },
    
    renderImplementation: function(implementation){
        var html = document.getElementById('implementation-item-template').innerHTML,
            el = document.createElement('div'),
            template = _.template(html),
            stakeholder = null,
            coordId = implementation.get('coordinating_stakeholder'),
            implDiv = this.el.querySelector('#implementations'),
            _this = this;
        
        implDiv.appendChild(el);
        for (var i = 0; i < this.stakeholderCategories.length; i++){
            stakeholder = this.stakeholderCategories.at(i).stakeholders.get(coordId);
            if (stakeholder != null) break;
        }
        el.innerHTML = template({ implementation: implementation, stakeholder: stakeholder });
        
        var editBtn = el.querySelector('.edit'),
            removeBtn = el.querySelector('.remove'),
            addBtn = el.querySelector('.add');
        
        editBtn.addEventListener('click', function(){
            _this.editImplementation(implementation, el);
        })
        
        removeBtn.addEventListener('click', function(){
            var message = gettext('Do you really want to delete the implementation and all of its solutions?');
            _this.confirm({ message: message, onConfirm: function(){
                implementation.destroy({
                    success: function() { implDiv.removeChild(el); },
                    error: _this.onError
                })
            }});
        })
        
        var SolutionsInImpl = Backbone.Collection.extend({
                url: config.api.solutionsInImplementation.format(this.caseStudy.id, implementation.id)
            }),
            solutionsInImpl = new SolutionsInImpl();
        
        solutionsInImpl.fetch({
            success: function(){ 
                solutionsInImpl.forEach(function(solInImpl){
                    _this.renderSolution(solInImpl, implementation, el);
                })
            }
        });
        
        var addModal = this.el.querySelector('#add-solution-modal');
        addBtn.addEventListener('click', function(){
            _this.confirmNewSolution = function(){
                var solutionId = _this.el.querySelector('#solution-select').value;
                var solInImpl = solutionsInImpl.create(
                    {
                        solution: solutionId
                    }, 
                    { 
                        wait: true,
                        success: function(){
                            $(addModal).modal('hide');
                            var solItem = _this.renderSolution(solInImpl, implementation, el);
                            _this.editSolution(solInImpl, implementation, solItem);
                        },
                        error: function(model, response) { _this.onError(response) }
                    },
                )
            };
            
        
            var solutionSelect = addModal.querySelector('#solution-select');
            
            solutionSelect.selectedIndex = 0;
            $(solutionSelect).selectpicker('refresh');
            
            $(addModal).modal('show');
        })
    },
    
    renderSolution: function(solutionInImpl, implementation, implementationItem){
        var html = document.getElementById('solution-item-template').innerHTML,
            el = document.createElement('div'),
            template = _.template(html),
            solDiv = implementationItem.querySelector('.solutions'),
            solId = solutionInImpl.get('solution'),
            _this = this;
        
        solDiv.appendChild(el);
        var solution;
        for (var i = 0; i < this.solutionCategories.length; i++){
            solution = this.solutionCategories.at(i).solutions.get(solId);
            if (solution != null) break;
        }
        
        el.innerHTML = template({ solutionInImpl: solutionInImpl, solution: solution });
        
        var editBtn = el.querySelector('.edit'),
            removeBtn = el.querySelector('.remove');
        
        editBtn.addEventListener('click', function(){
            _this.editSolution(solutionInImpl, implementation, el);
        })
        
        removeBtn.addEventListener('click', function(){
            var message = gettext('Do you really want to delete your solution?');
            _this.confirm({ message: message, onConfirm: function(){
                solutionInImpl.destroy({
                    success: function() { solDiv.removeChild(el); },
                    error: _this.onError
                })
            }});
        })
        this.renderSolutionPreviewMap(solutionInImpl, el);
        return el;
    },
    
    editImplementation: function(implementation, item){
        var modal = this.el.querySelector('#implementation-modal'),
            nameInput = modal.querySelector('#implementation-name-input'),
            coordSelect = modal.querySelector('#coordinator-select'),
            _this = this;
        
        nameInput.value = implementation.get('name');
        coordSelect.value = implementation.get('coordinating_stakeholder');
        $(coordSelect).selectpicker('refresh');
        
        this.confirmImplementation = function(){
            implementation.save(
                { 
                    name: nameInput.value, 
                    coordinating_stakeholder: coordSelect.value
                }, 
                {
                    success: function(){
                        item.querySelector('.title').innerHTML = nameInput.value;
                        item.querySelector('.coordinator').innerHTML = coordSelect[coordSelect.selectedIndex].text;
                        $(modal).modal('hide');
                },
                error: function(m, r){ _this.onError(r) }
            })
        };
        
        $(modal).modal('show');
    
    
    },
    
    addImplementation: function(){
        var modal = this.el.querySelector('#implementation-modal'),
            nameInput = modal.querySelector('#implementation-name-input'),
            coordSelect = modal.querySelector('#coordinator-select'),
            _this = this;
        
        nameInput.value = '';
        coordSelect.selectedIndex = 0;
        $(coordSelect).selectpicker('refresh');
        
        this.confirmImplementation = function(){
            var implementation = _this.implementations.create(
                {
                    name: nameInput.value,
                    coordinating_stakeholder: coordSelect.value
                }, 
                { 
                    wait: true,
                    success: function(){
                        _this.renderImplementation(implementation);
                        $(modal).modal('hide');
                    },
                    error: function(model, response) { _this.onError(response) }
                },
            )
        };
        
        $(modal).modal('show');
    },
    
    editSolution: function(solutionImpl, implementation, item, onConfirm){
        var _this = this;
        var html = document.getElementById('view-solution-implementation-template').innerHTML,
            template = _.template(html);
        var modal = this.el.querySelector('#solution-implementation-modal');
        
        var solution = null,
            solId = solutionImpl.get('solution');
        
        for (var i = 0; i < this.solutionCategories.length; i++){
            solution = this.solutionCategories.at(i).solutions.get(solId);
            if (solution != null) break;
        }
        
        modal.innerHTML = template({ 
            solutionCategories: this.solutionCategories,
            implementation: implementation,
            solutionImpl: solutionImpl,
            solution: solution,
            stakeholderCategories: this.stakeholderCategories
        });
        
        var select = modal.querySelector('.selectpicker');
        $(select).selectpicker();
        
        var Quantities = Backbone.Collection.extend({ 
            url: config.api.quantitiesInImplementedSolution.format(this.caseStudy.id, implementation.id, solutionImpl.id) })
        var squantities = new Quantities();
        
        var Ratios = Backbone.Collection.extend({ 
            url: config.api.solutionRatioOneUnits.format(this.caseStudy.id, solution.get('solution_category'), solution.id) })
        var sratios = new Ratios();
        
        squantities.fetch({success: function(){
            var table = modal.querySelector('#implemented-quantities');
            squantities.forEach(function(quantity){
                var row = table.insertRow(-1);
                row.insertCell(-1).innerHTML = quantity.get('name');
                var input = document.createElement('input');
                input.type = 'number';
                input.value = quantity.get('value');
                input.classList.add('form-control');
                row.insertCell(-1).appendChild(input);
                row.insertCell(-1).innerHTML = quantity.get('unit');
            });
        }});
        sratios.fetch({success: function(){
            var div = modal.querySelector('#ratios');
            sratios.forEach(function(ratio){
                var li = document.createElement('li');
                li.innerHTML = ratio.get('name') + ': ' + ratio.get('value') + ' ' + (_this.units.get(ratio.get('unit')).get('name'));
                div.appendChild(li);
            });
        }});
        this.renderEditorMap('editor-map', solutionImpl);
        $(modal).off();
        $(modal).on('shown.bs.modal', function () {
            _this.editorMap.map.updateSize();
        });
        $(modal).modal('show');
        
        var okBtn = modal.querySelector('.confirm');
        okBtn.addEventListener('click', function(){
            var features = _this.drawingSource.getFeatures();
            var multiPolygon = new ol.geom.MultiPolygon();
            features.forEach(function(feature) {
                var polygon = new ol.geom.Polygon(feature.getGeometry().getCoordinates());
                multiPolygon.appendPolygon(polygon);
             });
            var geoJSON = new ol.format.GeoJSON(),
                geoJSONText = geoJSON.writeGeometry(multiPolygon);
            var notes = modal.querySelector('textarea[name="description"]').value
            solutionImpl.set('notes', notes);
            solutionImpl.set('geom', geoJSONText);
            solutionImpl.save(null, {
                success: function(){
                    _this.renderSolutionPreviewMap(solutionImpl, item);
                    item.querySelector('textarea[name="notes"]').value = notes;
                    $(modal).modal('hide');
                },
                error: function(m, r){ _this.onError(r) }
            })
        })
    },
    
    renderSolutionPreviewMap: function(solutionImpl, item){
        var divid = 'solutionImpl' + solutionImpl.id;
        var mapDiv = item.querySelector('.map');
        mapDiv.id = divid;
        mapDiv.innerHTML = '';
        previewMap = new Map({
            divid: divid, 
        });
        var geom = solutionImpl.get('geom');
        //previewMap.addLayer('geometry', {
            //stroke: 'rgb(252, 195, 25)',
            //fill: 'rgba(252, 195, 25, 0.2)',
            //strokeWidth: 1,
            //zIndex: 1
        //});
        // add polygon of focusarea to both maps and center on their centroid
        if (geom != null){
            //var poly = previewMap.addPolygon(geom.coordinates, { projection: this.projection, layername: 'geometry', type: 'MultiPolygon'});
            //console.log(poly)
            //previewMap.centerOnPolygon(poly, { projection: this.projection });
        
            var feature = new ol.Feature({ geometry: new ol.geom.MultiPolygon(geom.coordinates) });
            
            var source = new ol.source.Vector({wrapX: false});
            source.addFeature(feature);
            var vector = new ol.layer.Vector({
                source: source
            });
            previewMap.map.addLayer(vector);
            previewMap.map.getView().fit(source.getExtent(), previewMap.map.getSize());
        };
    },
    
    renderEditorMap: function(divid, solutionImpl, activities){
        var _this = this;
        // remove old map
        if (this.editorMap){
            this.editorMap.map.setTarget(null);
            this.editorMap.map = null;
            this.editorMap = null;
        }
        this.editorMap = new Map({
            divid: divid, 
        });
        var focusarea = this.caseStudy.get('properties').focusarea;

        this.editorMap.addLayer('background', {
            stroke: '#aad400',
            fill: 'rgba(170, 212, 0, 0.1)',
            strokeWidth: 1,
            zIndex: 0
        });
        // add polygon of focusarea to both maps and center on their centroid
        if (focusarea != null){
            var poly = this.editorMap.addPolygon(focusarea.coordinates[0], { projection: this.projection, layername: 'background', tooltip: gettext('Focus area') });
            this.editorMap.centerOnPolygon(poly, { projection: this.projection });
        };
        //var deferreds = [];
        
        //activities.forEach(function(activityId){
            //_this.renderActivityOnMap(activityId);
        //})
        var map = this.editorMap.map;
        var geom = solutionImpl.get('geom');
        this.drawingSource = new ol.source.Vector({wrapX: false});
        if (geom){
            var feature = new ol.Feature({ geometry: new ol.geom.MultiPolygon(geom.coordinates) });
            this.drawingSource.addFeature(feature);
        }
        var vector = new ol.layer.Vector({
            source: this.drawingSource
        });
        map.addLayer(vector);
        var draw = new ol.interaction.Draw({
          source: this.drawingSource,
          type: 'Polygon'
        });
        map.addInteraction(draw);
    },

});
return ImplementationsView;
}
);
