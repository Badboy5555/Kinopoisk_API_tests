from selenium.common.exceptions import TimeoutException
from pages.base import BasePage
from locators.locators import ReviewsPageLocators


class ReviewsPage(BasePage):
    locators = ReviewsPageLocators()

    def save_reviews_to_json(self, name: str) -> None:
        """ Сохраняет рецинзии о фолиьме в файл в формате JSON по пути film_data/info """
        try:
            select = self.element_is_clickable(self.locators.COUNT_PER_PAGE_SELECTOR_TOP)
        except TimeoutException:
            select = False
        else:
            self.select_value_by_index(select, -1)
        finally:
            all_reviews = {
                'review': {'bad': {'count': 0, 'text': []},
                           'good': {'count': 0, 'text': []},
                           'neutral': {'count': 0, 'text': []}
                           }}

            next_page_button = self.elements_are_present(self.locators.PAGINATOR_NEXT_PAGE_BUTTON)

            while select is False or not next_page_button or next_page_button[-2] == '»':
                bad_reviews = self.elements_are_present(self.locators.REVIEW_NEGATIVE)
                good_reviews = self.elements_are_present(self.locators.REVIEW_POSITIVE)
                neutral_reviews = self.elements_are_present(self.locators.REVIEW_NEUTRAL)

                if bad_reviews:
                    for i in bad_reviews:
                        all_reviews['review']['bad']['count'] += 1
                        all_reviews['review']['bad']['text'].append(i.find_element(*self.locators.REVIEW_TEXT).text)

                if good_reviews:
                    for i in good_reviews:
                        all_reviews['review']['good']['count'] += 1
                        all_reviews['review']['good']['text'].append(i.find_element(*self.locators.REVIEW_TEXT).text)

                if neutral_reviews:
                    for i in neutral_reviews:
                        all_reviews['review']['neutral']['count'] += 1
                        all_reviews['review']['neutral']['text'].append(i.find_element(*self.locators.REVIEW_TEXT).text)

                if select and next_page_button:
                    next_page_button[-2].click()
                else:
                    break
        self.save_info_to_json(all_reviews, './film_data/info/', f'{name}_reviews')
