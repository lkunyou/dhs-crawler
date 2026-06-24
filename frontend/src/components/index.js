import BaseForm from './BaseForm.vue'
import BaseTable from './BaseTable.vue'
import TableSearch from './TableSearch.vue'
import FormField from './FormField.vue'
import DialogForm from './DialogForm.vue'

export {
  BaseForm,
  BaseTable,
  TableSearch,
  FormField,
  DialogForm
}

export default {
  install(app) {
    app.component('BaseForm', BaseForm)
    app.component('BaseTable', BaseTable)
    app.component('TableSearch', TableSearch)
    app.component('FormField', FormField)
    app.component('DialogForm', DialogForm)
  }
}