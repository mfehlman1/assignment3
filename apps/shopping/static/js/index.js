"use strict";

// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


app.data = {
    data: function() {
        return {
            // Complete as you see fit.
            items: [],
            newItem: '',
        };
    },
    methods: {
        // Complete as you see fit.
        loadItems()
        {
            fetch(load_data_url)
            .then(response => response.json())
            .then(data => {
                this.items = data.items;
            });
        },

        add()
        {
            if (this.newItem.trim())
            {
                fetch(add_item_url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ item_name: this.newItem})
                })
                .then(response => response.json()) 
                .then(data => {
                    if (data.status === 'success'){
                        this.newItem = '';
                        this.loadItems();
                    }
                });
            }
        },

        purchased(item)
        {
            fetch(update_item_url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ item_id: item.id, is_purchased: !item.is_purchased })
            })
            .then(response => response.json()) 
            .then(data => {
                if (data.status === 'Success'){
                    this.loadItems();
                }
            });
        },

        delete(itemId)
        {
            fetch(delete_item_url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ item_id: itemId })
            })
            .then(response => response.json()) 
            .then(data => {
                if (data.status === 'Success'){
                    this.loadItems();
                }
            })
        }

    },
    created() {
        this.loadItems();
    }
};

app.vue = Vue.createApp(app.data).mount("#app");

app.load_data = function () {
    // Complete.
    app.vue.loadItems();
}

// This is the initial data load.
app.load_data();

