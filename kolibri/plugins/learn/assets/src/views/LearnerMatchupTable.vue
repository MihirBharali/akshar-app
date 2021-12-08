<template>

  <CoreTable>
    <template #headers>
      <th v-for="(value, key) in tableHeaders" :key="`${value}-${key}`">
        {{ value }}
      </th>
    </template>
    <template #tbody>
      <tbody>
        <tr v-for="rowObj in tableBodyData" :key="rowObj.id">
          <td v-for="(__value, key) in tableHeaders" :key="`${__value}-${key}-${rowObj.id}`">
            {{ rowObj[key] }}
          </td>
        </tr>
      </tbody>
    </template>
  </CoreTable>

</template>
<script>

  import CoreTable from 'kolibri.coreVue.components.CoreTable';

  export default {
    name: 'LearnerMatchupTable',
    components: { CoreTable },
    props: ['tableHeaders', 'tableBodyData'],
  };

</script>