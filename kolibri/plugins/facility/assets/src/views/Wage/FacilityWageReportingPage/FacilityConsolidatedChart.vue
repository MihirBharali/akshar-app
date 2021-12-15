<template>

  <div>
    <KPageContainer class="container">

      <h2> {{ $tr('headerTitle') }}</h2>  
      <p> {{ $tr('subHeaderText') }}</p>

      <KGrid gutter="16" :debug="false">
        <KGridItem :layout12="{ span: 4 }" />
        <KGridItem :layout12="{ span: 3 }">
          From: <Datepicker v-model="startDate" placeholder="Select Start Date" class="startDate" />

        </KGridItem>
        <KGridItem :layout12="{ span: 3 }">
          To:
          <Datepicker v-model="endDate" placeholder="Select Start Date" />

        </KGridItem>
        <KGridItem :layout12="{ span: 2 }">
          <KButton :primary="true" text="Go" appearance="raised-button" class="move-down" @click="filterByDateRange" />
        </KGridItem>


      </KGrid>


      <CoreTable
        :selectable="true"
        :emptyMessage="$tr('searchNoResultText')"
        class="move-down"
      >

        <template #headers>
          <th> {{ $tr('reasonLabel') }}</th>
          <th>{{ $tr('depositLabel') }}</th>
          <th>{{ $tr('withdrawalLabel') }}</th>
        </template>    
        <template #tbody>
          <tbody>
            <tr v-for="(__value, key) in depositTransactions" :key="`${__value}-${key}`">
              <td> {{ key }}</td>
              <td>
                {{ __value }}
              </td><td></td>
            </tr>
            <tr v-for="(__value, key) in withdrawalTransactions" :key="`${__value}-${key}`">
              <td> {{ key }}</td>
              <td> </td>
              <td>{{ __value }}</td>
            </tr>
            <tr class="total">
              <td> {{ $tr('totalLabel') }} </td>
              <td> {{ totalDeposits }}</td>
              <td> {{ totalWithdrawals }}</td>
            </tr>
          </tbody>
        </template>       

      </CoreTable>



    </KPageContainer>
  </div>

</template>


<script>

  import { mapState } from 'vuex';
  import Datepicker from 'vuejs-datepicker';
  import CoreTable from 'kolibri.coreVue.components.CoreTable';
  import PaginatedListContainer from 'kolibri.coreVue.components.PaginatedListContainer';

  export default {
    name: 'FacilityConsolidatedChartPage',
    components: { PaginatedListContainer, CoreTable, Datepicker },
    mixins: [],
    computed: {
      ...mapState('wage', ['facilityAllWageRequests', 'defaultStartDate', 'defaultEndDate']),
      startDateFormatted() {
        return this.formatDate(this.start);
      },
    },
    watch: {
      facilityAllWageRequests(requests, oldRequests) {
        this.setData();
      },
    },
    beforeMount() {
      this.init();
    },
    data() {
      return {
        startDate: null,
        endDate: null,
        totalDeposits: 0,
        totalWithdrawals: 0,
        depositTransactions: {},
        withdrawalTransactions: {},
      };
    },
    methods: {
      init() {
        this.startDate = new Date(this.defaultStartDate);
        this.endDate = new Date(this.defaultEndDate);
        this.setData();
      },
      setData() {
        this.totalDeposits = 0;
        this.totalWithdrawals = 0;
        this.depositTransactions = {};
        this.withdrawalTransactions = {};
        this.facilityAllWageRequests.forEach(item => {
          if (item['request_type'] == 'CREDIT') {
            let currentTotal = this.depositTransactions[item['reason']];
            this.totalDeposits += item['transaction_amount'];
            if (currentTotal === undefined) {
              this.depositTransactions[item['reason']] = item['transaction_amount'];
            } else {
              this.depositTransactions[item['reason']] = currentTotal + item['transaction_amount'];
            }
          } else {
            let currentTotal = this.withdrawalTransactions[item['reason']];
            this.totalWithdrawals += item['transaction_amount'];
            if (currentTotal === undefined) {
              this.withdrawalTransactions[item['reason']] = item['transaction_amount'];
            } else {
              this.withdrawalTransactions[item['reason']] =
                currentTotal + item['transaction_amount'];
            }
          }
        });
      },

      formatDate(date) {
        if (date === null) {
          return '';
        }
        let year = date.getFullYear();
        let month = date.getMonth() + 1;
        let day = date.getDate();
        let str = year + '-' + month + '-' + day;
        return str;
      },
      filterByDateRange() {
        let startingDate = this.formatDate(this.startDate);
        let endingDate = this.formatDate(this.endDate);
        this.$store
          .dispatch('wage/getTransactionsByDateRange', {
            startDate: startingDate,
            endDate: endingDate,
            facilityId: this.$store.getters.activeFacilityId,
          })
          .then(transactions => {
            this.$store.commit('wage/UPDATE_CONSOLIDATED_CHART_WAGE_DETAILS', {
              facilityAllWageRequests: transactions,
            });
          })
          .catch(err => {
            this.$store.dispatch('handleApiError', err);
          });
      },
    },
    $trs: {
      headerTitle: 'Consolidated report',
      subHeaderText: 'Details regarding transactions for each withdrawal and deposit methods',
      searchNoResultText: 'No matching transaction found',
      learnerLabel: 'Student',
      dateLable: 'Date',
      reasonLabel: 'Reason',
      depositLabel: 'Deposit',
      withdrawalLabel: 'Withdrwal',
      dateFilterFrom: 'From:',
      dateFilterTo: 'To:',
      dateFilterButton: 'Go',
      totalLabel: 'Total',
    },
  };

</script>


<style lang="scss" >

  .move-down {
    position: relative;
    margin-top: 16px;
  }
  .container {
    height: 500px !important;
  }

  .total {
    font-weight: bold;
  }

</style>
