<template>
  <div>
    <div v-if="isLoaded">
      <h2 class="gh__title">Scribe</h2>
      <div class="gh__container">
        <div v-for="prType in prTypes" key="0" class="gh__type-container">
          <h3 class="gh__type-title">{{ prType[0] }}</h3>
          <h4 v-if="prType[1].length === 0">All Set Here!</h4>
          <div v-for="pr in prType[1]" key="url" class="gh__pr-container">
            <a class="gh__pr-title" target="_blank" :href="pr.html_url">{{ pr.title }}</a>
            <p v-html="$options.filters.markdown(pr.body)"></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Remarkable from 'remarkable';

const md = new Remarkable();

export default {
  name: 'git-hub',
  created() {
    const vthis = this;
    return axios.get('/start-api/v1/github')
      .then((response) => {
        response.data['review-requests'].forEach((pr) => { vthis.reviewRequests.push(pr); });
        response.data.approved.forEach((pr) => { vthis.approved.push(pr); });
        response.data['changes-requested'].forEach((pr) => { vthis.changesRequested.push(pr); });
        vthis.isLoaded = true;
      });
  },
  computed: {
    prTypes() {
      return [
        ['Review Requests', this.reviewRequests],
        ['Approved', this.approved],
        ['Changes Requested', this.changesRequested],
      ];
    },
  },
  data() {
    return {
      isLoaded: false,
      reviewRequests: [],
      approved: [],
      changesRequested: [],
    };
  },
  filters: {
    markdown(value) {
      return md.render(value);
    },
  },
};
</script>  

<style lang="scss" scoped>
@import "../styles/global.scss";
.gh {
    &__title {
        @include shadow;
        font-size: 3rem;
        margin-top: 2rem;
    }
    &__container {
        background-color: $bg-color;
        margin: 16px 0;
        display: flex;
        flex-wrap: wrap;
        align-items: stretch;
        color: $fg-color-primary;
    }
    &__type-container {
        padding: 2rem;
        width: calc(33% - 4rem);
        @include breakpoint(xs) {
            width: calc(100% - 4rem);
        }
    }
    &__type-title {
        font-size: 1.8rem;
        color: $fg-color-light-purple;
        padding: 1rem 0;
    }
    &__pr-container {
        overflow: scroll;
    }
    &__pr-title {
        display: inline-block;
        font-size: 1.8rem;
        font-weight: bold;
        text-decoration: underline;
        color: #79b2a8;
        margin: 1rem 0;
    }
    &__pr-title:visited, &__pr-title:active {
        color: #79b2a8;
    }
    &__pr-title:hover {
	    color: #1a8976;
    }
}
  
</style>
