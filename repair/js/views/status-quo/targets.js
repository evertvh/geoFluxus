define(['backbone', 'underscore'],

function(Backbone, _,){
    /**
    *
    * @author Christoph Franke
    * @name module:views/TargetsView
    * @augments Backbone.View
    */
    var TargetsView = Backbone.View.extend(
        /** @lends module:views/TargetsView.prototype */
        {

        /**
        * render setup view on targets
        *
        * @param {Object} options
        * @param {HTMLElement} options.el                      element the view will be rendered in
        * @param {string} options.template                     id of the script element containing the underscore template to render this view
        * @param {module:models/CaseStudy} options.caseStudy   the casestudy to add targets to
        *
        * @constructs
        * @see http://backbonejs.org/#View
        */
        initialize: function(options){
            var _this = this;
            _.bindAll(this, 'render');

            this.template = options.template;
            this.caseStudy = options.caseStudy;
            this.mode = options.mode || 0;
            
            this.aims = [
                'Higher Recycling rate',
                'Less non recyclable garbage'
            ]
            
            this.indicators = {
                'Higher Recycling rate': [
                    'Indicator AB',
                    'Indicator XY',
                ],
                'Less non recyclable garbage': []
            };
            
            this.targets = [
                'reduce by 50%',
                'reduce by 30%',
                'reduce by 15%',
                'reduce by 10%',
                'reduce by 5%',
                'increase by 5%',
                'increase by 10%',
                'increase by 15%',
                'increase by 30%',
                'increase by 50%',
            ];
            
            this.spatial = [ 'Focus Area', 'Study Area' ]
            
            this.render();
        },

        /*
        * dom events (managed by jquery)
        */
        events: {
        },

        /*
        * render the view
        */
        render: function(){
            var _this = this;
            var html = document.getElementById(this.template).innerHTML
            var template = _.template(html);
            this.el.innerHTML = template();
            this.renderRows();
            
            // lazy way to render workshop mode: just hide all buttons for editing
            // you may make separate views as well
            if (this.mode == 0){
                var btns = this.el.querySelectorAll('button.add, button.edit, button.remove');
                _.each(btns, function(button){
                    button.style.display = 'none';
                });
            }
        },

        renderRows(){
            var _this = this;
            this.aims.forEach(function(aim){
                var row = document.createElement('div');
                row.classList.add('row', 'overflow', 'bordered');
                var html = document.getElementById('target-row-template').innerHTML
                var template = _.template(html);
                row.innerHTML = template({ aim: aim });
                _this.el.appendChild(row);
                var indicatorPanel = row.querySelector('.indicators').querySelector('.item-panel'),
                    targetPanel = row.querySelector('.targets').querySelector('.item-panel'),
                    spatialPanel = row.querySelector('.spatial').querySelector('.item-panel'),
                    html = document.getElementById('panel-item-template').innerHTML
                    template = _.template(html);
                var indicators = _this.indicators[aim];
                indicators.forEach(function(indicator){
                    var panelItem = document.createElement('div');
                    panelItem.classList.add('panel-item');
                    panelItem.innerHTML = template({ name: indicator });
                    indicatorPanel.appendChild(panelItem);
                    
                    var targetSelect = document.createElement('select');
                    targetSelect.classList.add('panel-item', 'form-control');
                    _this.targets.forEach(function(target){
                        var option = document.createElement('option');
                        option.text = target;
                        targetSelect.appendChild(option);
                    })
                    targetPanel.appendChild(targetSelect);
                    
                    var spatialSelect = document.createElement('select');
                    spatialSelect.classList.add('panel-item', 'form-control');
                    _this.spatial.forEach(function(s){
                        var option = document.createElement('option');
                        option.text = s;
                        spatialSelect.appendChild(option);
                    })
                    spatialPanel.appendChild(spatialSelect);
                })
            })
        },

        /*
        * remove this view from the DOM
        */
        close: function(){
            this.undelegateEvents(); // remove click events
            this.unbind(); // Unbind all local event bindings
            this.el.innerHTML = ''; //empty the DOM element
        },

    });
    return TargetsView;
}
);