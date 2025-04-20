from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time


@allure.feature("Тестовые сценарии для сайта Pizzeria")
class TestCases:
    @allure.story("Добавление пицц в корзину и проверка содержимого")
    @allure.description(
        "Этот тест добавляет три разные пиццы в корзину и проверяет их наличие"
    )
    def test_case_1(self, set_up_browser):
        driver = set_up_browser

        with allure.step("Открытие главной страницы сайта"):
            driver.get("https://pizzeria.skillbox.cc/")

        with allure.step('Добавление пиццы "Рай" в корзину'):
            WebDriverWait(driver, 3)
            pizza_one = driver.find_element(By.XPATH, '(//*[@title= "Пицца «Рай»"])[3]')
            ActionChains(driver).move_to_element(pizza_one).perform()
            driver.find_element(
                By.XPATH, '(//*[contains(text(), "В корзину")])[7]'
            ).click()

        with allure.step('Добавление пиццы "Пепперони" в корзину'):
            driver.find_element(By.CLASS_NAME, "slick-next").click()
            WebDriverWait(driver, 3)
            pizza_two = driver.find_element(
                By.XPATH, '(//*[@title= "Пицца «Пепперони»"])[3]'
            )
            ActionChains(driver).move_to_element(pizza_two).perform()
            driver.find_element(
                By.XPATH, '(//*[contains(text(), "В корзину")])[9]'
            ).click()

        with allure.step('Добавление пиццы "4 в 1" в корзину'):
            driver.find_element(By.CLASS_NAME, "slick-prev").click()
            WebDriverWait(driver, 3)
            pizza_three = driver.find_element(
                By.XPATH, '(//*[@title= "Пицца «4 в 1»"])[1]'
            )
            ActionChains(driver).move_to_element(pizza_three).perform()
            driver.find_element(
                By.XPATH, '(//*[contains(text(), "В корзину")])[5]'
            ).click()
            time.sleep(2)

        with allure.step("Проверка содержимого корзины"):
            driver.find_element(By.CLASS_NAME, "cart-contents").click()
            products_in_cart = driver.find_elements(By.CLASS_NAME, "product-name")
            expected_products = ["Пицца «Рай»", "Пицца «Пепперони»", "Пицца «4 в 1»"]
            expected_products_normalized = [
                product.replace("«", '"').replace("»", '"')
                for product in expected_products
            ]
            actual_products = [
                product.text for product in products_in_cart if product.text != "ТОВАР"
            ]

            for expected_product in expected_products_normalized:
                with allure.step(
                    f'Проверка наличия товара "{expected_product}" в корзине'
                ):
                    assert (
                        expected_product in actual_products
                    ), f"Товар {expected_product} отсутствует в корзине"

            allure.attach(
                "Все выбранные товары присутствуют в корзине.",
                name="Результат проверки",
                attachment_type=allure.attachment_type.TEXT,
            )

    @allure.story("Заказ пиццы с дополнительными опциями")
    @allure.description(
        """
    Этот тест выполняет следующие действия:
    1. Открывает главную страницу сайта Pizzeria.
    2. Выбирает пиццу "Как у бабушки".
    3. Добавляет дополнительную опцию "Сырный борт".
    4. Добавляет пиццу в корзину.
    5. Проверяет содержимое корзины на наличие заказанной пиццы с дополнительной опцией.
    """
    )
    def test_case_2(self, set_up_browser):
        driver = set_up_browser

        with allure.step("Открытие главной страницы сайта"):
            driver.get("https://pizzeria.skillbox.cc/")
            WebDriverWait(driver, 3)

        with allure.step('Выбор пиццы "Как у бабушки"'):
            driver.find_element(
                By.XPATH, '(//*[@title= "Пицца «Как у бабушки»"])[3]'
            ).click()
            WebDriverWait(driver, 3)

        with allure.step('Добавление дополнительной опции "Сырный борт"'):
            driver.find_element(By.NAME, "board_pack").click()
            driver.find_element(
                By.XPATH, "//*[contains(text(), 'Сырный - 55.00 р.')]"
            ).click()

        with allure.step("Добавление пиццы в корзину"):
            driver.find_element(By.CLASS_NAME, "single_add_to_cart_button").click()
            time.sleep(2)

        with allure.step("Проверка содержимого корзины"):
            driver.find_element(By.CLASS_NAME, "cart-contents").click()
            time.sleep(2)
            products_in_cart = driver.find_elements(By.CLASS_NAME, "product-name")
            expected_products = ['Пицца "Как у бабушки"\nДополнительно:\nСырный борт']
            expected_products_normalized = [
                product.replace("«", '"').replace("»", '"')
                for product in expected_products
            ]
            actual_products = [
                product.text for product in products_in_cart if product.text != "ТОВАР"
            ]

            for expected_product in expected_products_normalized:
                with allure.step(
                    f'Проверка наличия товара "{expected_product}" в корзине'
                ):
                    assert (
                        expected_product in actual_products
                    ), f"Товар {expected_product} отсутствует в корзине"

            allure.attach(
                "Все выбранные товары присутствуют в корзине.",
                name="Результат проверки",
                attachment_type=allure.attachment_type.TEXT,
            )

    @allure.story("Управление корзиной и проверка итоговой суммы")
    @allure.description(
        """
    Этот тест выполняет следующие действия:
    1. Открывает главную страницу сайта Pizzeria.
    2. Добавляет пиццу "Рай" в корзину.
    3. Выбирает пиццу "Как у бабушки" с дополнительной опцией "Сырный борт" и добавляет в корзину.
    4. Открывает корзину.
    5. Увеличивает количество первой пиццы на 1.
    6. Обновляет корзину.
    7. Удаляет вторую пиццу из корзины.
    8. Проверяет, что общая сумма корзины равна 1030,00 руб.
    """
    )
    def test_case_3(self, set_up_browser):
        driver = set_up_browser

        with allure.step("Открытие главной страницы сайта"):
            driver.get("https://pizzeria.skillbox.cc/")
            time.sleep(0.2)

        with allure.step('Добавление пиццы "Рай" в корзину'):
            pizza_one = driver.find_element(By.XPATH, '(//*[@title= "Пицца «Рай»"])[3]')
            ActionChains(driver).move_to_element(pizza_one).perform()
            time.sleep(0.2)
            driver.find_element(
                By.XPATH, '(//*[contains(text(), "В корзину")])[7]'
            ).click()

        with allure.step('Добавление пиццы "Как у бабушки" с сырным бортом в корзину'):
            pizza_two = driver.find_element(
                By.XPATH, '(//*[@title= "Пицца «Как у бабушки»"])[3]'
            )
            pizza_two.click()
            time.sleep(0.2)
            driver.find_element(By.NAME, "board_pack").click()
            driver.find_element(
                By.XPATH, "//*[contains(text(), 'Сырный - 55.00 р.')]"
            ).click()
            driver.find_element(By.CLASS_NAME, "single_add_to_cart_button").click()
            time.sleep(2)

        with allure.step("Открытие корзины"):
            driver.find_element(By.CLASS_NAME, "cart-contents").click()
            time.sleep(2)

        with allure.step("Увеличение количества первой пиццы"):
            driver.find_element(By.XPATH, '(//input[@ title="Кол-во"])[1]').click()
            action_chains = ActionChains(driver)
            action_chains.send_keys(Keys.ARROW_UP)
            action_chains.perform()

        with allure.step("Обновление корзины"):
            driver.find_element(By.NAME, "update_cart").click()
            time.sleep(2)

        with allure.step("Удаление второй пиццы из корзины"):
            driver.find_element(By.XPATH, '(//a[@class ="remove"])[2]').click()
            time.sleep(2)

        with allure.step("Проверка общей суммы корзины"):
            wait = WebDriverWait(driver, 10)
            total_price_element = wait.until(
                EC.presence_of_element_located((By.XPATH, "(//bdi)[4]"))
            )
            total_price = total_price_element.text

            with allure.step("Проверка, что общая сумма равна 1030,00 руб"):
                assert (
                    total_price == "1030,00₽"
                ), f"Ожидаемая сумма: 1030,00 руб, но получено: {total_price}"

            allure.attach(
                "Общая сумма корзины равна 1030,00 руб.",
                name="Результат проверки",
                attachment_type=allure.attachment_type.TEXT,
            )

    @allure.story("Фильтрация десертов по цене и добавление в корзину")
    @allure.description(
        """
    Этот тест выполняет следующие действия:
    1. Открывает главную страницу сайта Pizzeria.
    2. Переходит в раздел "Десерты" через меню.
    3. Устанавливает фильтр цены до 135 руб.
    4. Проверяет, что все отображаемые десерты имеют цену не выше 135 руб.
    5. Добавляет первый десерт в корзину.
    6. Проверяет наличие добавленного десерта в корзине.
    """
    )
    def test_case_4(self, set_up_browser):
        driver = set_up_browser

        with allure.step("Открытие главной страницы сайта"):
            driver.get("https://pizzeria.skillbox.cc/")
            time.sleep(0.2)

        with allure.step('Переход в раздел "Десерты"'):
            menu = driver.find_element(
                By.XPATH, '//nav/div/ul/li/a[contains(text(), "Меню")]'
            )
            action_chains = ActionChains(driver)
            action_chains.move_to_element(menu).perform()
            driver.find_element(
                By.XPATH, '//ul/li//ul/li/a[contains(text(), "Десерты")]'
            ).click()
            time.sleep(2)

        with allure.step("Установка фильтра цены до 135 руб"):
            range = driver.find_element(
                By.XPATH,
                '(//span[@class="ui-slider-handle ui-state-default ui-corner-all"])[2]',
            )
            action_chains.click_and_hold(range).move_by_offset(
                xoffset=-170, yoffset=0
            ).perform()
            action_chains.release().perform()
            time.sleep(2)
            driver.find_element(
                By.XPATH, '//button[contains(text(), "Применить")]'
            ).click()
            time.sleep(2)

        with allure.step("Проверка фильтрации цен"):
            prices_elements = driver.find_elements(By.XPATH, "//div/span/span/bdi")
            prices = []
            for price_element in prices_elements:
                price_text = price_element.text.replace("₽", "").replace(",", ".")
                prices.append(float(price_text))

            all_prices_below_135 = all(price <= 135 for price in prices)
            assert all_prices_below_135, "Не все цены меньше 135 руб"
            allure.attach(
                "Все найденные элементы имеют цену меньше 135 руб",
                name="Результат фильтрации",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Добавление десерта в корзину"):
            driver.find_element(
                By.XPATH, '(//a[contains(text(), "В корзину")])[1]'
            ).click()
            time.sleep(2)

        with allure.step("Проверка наличия десерта в корзине"):
            driver.find_element(By.CLASS_NAME, "cart-contents").click()
            time.sleep(2)
            products_in_cart = driver.find_elements(By.CLASS_NAME, "product-name")
            expected_products = ['Десерт "Булочка с корицей"']
            expected_products_normalized = [
                product.replace("«", '"').replace("»", '"')
                for product in expected_products
            ]
            actual_products = [
                product.text for product in products_in_cart if product.text != "ТОВАР"
            ]

            for expected_product in expected_products_normalized:
                with allure.step(
                    f'Проверка наличия товара "{expected_product}" в корзине'
                ):
                    assert (
                        expected_product in actual_products
                    ), f"Товар {expected_product} отсутствует в корзине"

            allure.attach(
                "Все выбранные товары присутствуют в корзине.",
                name="Результат проверки корзины",
                attachment_type=allure.attachment_type.TEXT,
            )

    @allure.story("Регистрация нового пользователя")
    @allure.description(
        """
    Этот тест выполняет следующие действия:
    1. Открывает главную страницу сайта Pizzeria.
    2. Переходит на страницу "Мой аккаунт".
    3. Нажимает кнопку "Зарегистрироваться".
    4. Заполняет форму регистрации (имя пользователя, email, пароль).
    5. Отправляет форму регистрации.
    6. Проверяет успешность регистрации.
    7. Проверяет, что пользователь авторизован на сайте.
    """
    )
    def test_case_5(self, set_up_browser):
        driver = set_up_browser

        with allure.step("Открытие главной страницы сайта"):
            driver.get("https://pizzeria.skillbox.cc/")
            time.sleep(0.2)

        with allure.step('Переход на страницу "Мой аккаунт"'):
            my_account = driver.find_element(
                By.XPATH, '//nav/div/ul/li/a[contains(text(), "Мой аккаунт")]'
            )
            my_account.click()
            time.sleep(0.2)

        with allure.step('Нажатие кнопки "Зарегистрироваться"'):
            driver.find_element(
                By.XPATH, '//button[contains(text(), "Зарегистрироваться")]'
            ).click()

        with allure.step("Заполнение формы регистрации"):
            username = "Thomasss"
            email = "thomasss@cruise.com"
            password = "123456"

            username_field = driver.find_element(By.ID, "reg_username")
            for i in username:
                username_field.send_keys(i)
                time.sleep(0.2)

            email_field = driver.find_element(By.ID, "reg_email")
            for i in email:
                email_field.send_keys(i)
                time.sleep(0.2)

            password_field = driver.find_element(By.ID, "reg_password")
            for i in password:
                password_field.send_keys(i)
                time.sleep(0.2)

        with allure.step("Отправка формы регистрации"):
            driver.find_element(By.NAME, "register").click()
            time.sleep(2)

        with allure.step("Проверка успешной регистрации"):
            reg_succeed = driver.find_element(By.XPATH, "//article/div/div/div/div")
            reg_succeed_text = reg_succeed.text
            assert (
                "Регистрация завершена" in reg_succeed_text
            ), "Регистрация прошла неуспешно"
            allure.attach(
                "Регистрация завершена успешно",
                name="Результат регистрации",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Проверка авторизации пользователя"):
            time.sleep(2)
            driver.find_element(
                By.XPATH, '//nav/div/ul/li/a[contains(text(), "Мой аккаунт")]'
            ).click()
            greeting_name = driver.find_element(
                By.XPATH, '//*[@id="post-22"]/div/div/div/div/div/p[1]/strong'
            )
            greeting_name_text = greeting_name.text
            assert (
                username in greeting_name_text
            ), f"Пользователь {username} не был авторизован на сайте"
            allure.attach(
                f"Пользователь {username} успешно авторизован",
                name="Результат авторизации",
                attachment_type=allure.attachment_type.TEXT,
            )

    @allure.story("Оформление заказа авторизованным пользователем")
    @allure.description(
        """
    Этот тест выполняет следующие действия:
    1. Открывает главную страницу сайта Pizzeria.
    2. Авторизует пользователя.
    3. Добавляет товары в корзину.
    4. Переходит к оформлению заказа.
    5. Вводит данные для доставки.
    6. Проверяет итоговую сумму заказа.
    7. Размещает заказ.
    8. Проверяет детали оформленного заказа.
    """
    )
    def test_case_6(self, set_up_browser):
        driver = set_up_browser

        with allure.step("Открытие главной страницы сайта"):
            driver.get("https://pizzeria.skillbox.cc/")
            time.sleep(0.2)

        with allure.step("Авторизация пользователя"):
            my_account = driver.find_element(
                By.XPATH, '//nav/div/ul/li/a[contains(text(), "Мой аккаунт")]'
            )
            my_account.click()
            time.sleep(0.2)
            log_in_name = driver.find_element(By.NAME, "username")
            username = "Thomasss"
            for i in username:
                log_in_name.send_keys(i)
                time.sleep(0.2)
            log_in_password = driver.find_element(By.NAME, "password")
            password = "123456"
            for i in password:
                log_in_password.send_keys(i)
                time.sleep(0.2)
            driver.find_element(By.NAME, "login").click()
            time.sleep(2)

        with allure.step("Наполнение корзины"):
            driver.find_element(
                By.XPATH, '//nav/div/ul/li/a[contains(text(), "Меню")]'
            ).click()
            time.sleep(2)
            driver.find_element(
                By.XPATH, '(//div/div/a[contains(text(), "В корзину")])[1]'
            ).click()
            time.sleep(1)
            driver.find_element(
                By.XPATH, '(//div/div/a[contains(text(), "В корзину")])[10]'
            ).click()
            time.sleep(1)
            driver.find_element(
                By.XPATH, '(//div/div/a[contains(text(), "В корзину")])[4]'
            ).click()
            time.sleep(1)
            driver.find_element(By.CLASS_NAME, "cart-contents").click()
            time.sleep(2)
            driver.find_element(By.CLASS_NAME, "checkout-button").click()
            time.sleep(2)

        with allure.step("Ввод данных для доставки"):
            delivery_name = driver.find_element(By.NAME, "billing_first_name")
            delivery_name_text = "Tom"
            for i in delivery_name_text:
                delivery_name.send_keys(i)
                time.sleep(0.2)

            delivery_surname = driver.find_element(By.NAME, "billing_last_name")
            delivery_surname_text = "Cruise"
            for i in delivery_surname_text:
                delivery_surname.send_keys(i)
                time.sleep(0.2)

            dropdown_country = driver.find_element(
                By.ID, "select2-billing_country-container"
            )
            dropdown_country.click()
            wait = WebDriverWait(driver, 10)
            options = wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".select2-results__option")
                )
            )
            for option in options:
                if option.text == "United States (US)":
                    option.click()
                    break
            wait.until(
                EC.text_to_be_present_in_element(
                    (By.ID, "select2-billing_country-container"), "United States (US)"
                )
            )

            address = driver.find_element(By.NAME, "billing_address_1")
            home_address = "1111 Calle Vista Dr"
            for i in home_address:
                address.send_keys(i)
                time.sleep(0.2)

            city = driver.find_element(By.NAME, "billing_city")
            city_text = "Beverly Hills"
            for i in city_text:
                city.send_keys(i)
                time.sleep(0.2)

            dropdown_state = driver.find_element(
                By.CLASS_NAME, "select2-selection__placeholder"
            )
            dropdown_state.click()
            wait = WebDriverWait(driver, 10)
            options = wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".select2-results__option")
                )
            )
            for option in options:
                if option.text == "California":
                    option.click()
                    break

            time.sleep(2)
            postcode = driver.find_element(By.NAME, "billing_postcode")
            postcode_text = "90210"
            for i in postcode_text:
                postcode.send_keys(i)
                time.sleep(0.2)

            phone = driver.find_element(By.NAME, "billing_phone")
            phone_text = "+12345678900"
            for i in phone_text:
                phone.send_keys(i)
                time.sleep(0.2)

            date = driver.find_element(By.NAME, "order_date")
            date.click()
            order_date = "01/25/2025"
            for i in order_date:
                date.send_keys(i)
                time.sleep(0.5)

        with allure.step("Проверка итоговой суммы заказа"):
            total = driver.find_element(By.XPATH, "(//bdi)[5]")
            total_text = total.text
            assert "970,00₽" in total_text, "Итоговая сумма отличается от 970,00₽"
            allure.attach(
                f"Итоговая сумма заказа: {total_text}",
                name="Сумма заказа",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Размещение заказа"):
            driver.find_element(By.ID, "payment_method_cod").click()
            driver.find_element(By.ID, "terms").click()
            driver.find_element(By.ID, "place_order").click()

        with allure.step("Проверка деталей заказа"):
            time.sleep(2)
            email = driver.find_element(
                By.XPATH, "(//article/div/div/div/div/div/ul/li/strong)[3]"
            )
            email_text = email.text
            assert (
                "thomasss@cruise.com" in email_text
            ), "Некорректный адрес электронной почты"

            total_sum = driver.find_element(
                By.XPATH, "(//article/div/div/div/div/div/ul/li/strong)[4]"
            )
            total_sum_text = total_sum.text
            assert "970,00₽" in total_sum_text, "Некорректная сумма заказа"

            payment_method = driver.find_element(
                By.XPATH, "(//article/div/div/div/div/div/ul/li/strong)[5]"
            )
            payment_method_text = payment_method.text
            assert (
                "Оплата при доставке" in payment_method_text
            ), "Некорректный метод оплаты"

            products_in_order = driver.find_elements(By.CLASS_NAME, "product-name")
            expected_products = [
                "Айс латте × 1",
                'Десерт "Шоколадный шок" × 1',
                'Пицца "Пепперони" × 1',
            ]
            expected_products_normalized = [
                product.replace("«", '"').replace("»", '"')
                for product in expected_products
            ]
            actual_products = [
                product.text for product in products_in_order if product.text != "ТОВАР"
            ]
            for expected_product in expected_products_normalized:
                assert (
                    expected_product in actual_products
                ), f"Товар {expected_product} отсутствует в заказе"
            allure.attach(
                "Все выбранные товары присутствуют в заказе.",
                name="Проверка товаров",
                attachment_type=allure.attachment_type.TEXT,
            )

            address_in_order = driver.find_element(By.XPATH, "//address")
            address_in_order_text = address_in_order.text
            assert (
                "Tom Cruise\n1111 Calle Vista Dr\nBeverly Hills, CA 90210\nUnited States (US)"
                "\n+12345678900\nthomasss@cruise.com" in address_in_order_text
            ), "Некорректный адрес доставки"
            allure.attach(
                address_in_order_text,
                name="Адрес доставки",
                attachment_type=allure.attachment_type.TEXT,
            )

    @allure.story("Применение купона к заказу")
    @allure.description(
        """
    Этот тест выполняет следующие действия:
    1. Открывает главную страницу сайта Pizzeria.
    2. Авторизует пользователя.
    3. Добавляет товары в корзину.
    4. Применяет купон к заказу.
    5. Проверяет итоговую сумму заказа с учетом скидки.
    """
    )
    def test_case_7(self, set_up_browser):
        driver = set_up_browser

        with allure.step("Открытие главной страницы сайта"):
            driver.get("https://pizzeria.skillbox.cc/")
            time.sleep(0.2)

        with allure.step("Авторизация пользователя"):
            my_account = driver.find_element(
                By.XPATH, '//nav/div/ul/li/a[contains(text(), "Мой аккаунт")]'
            )
            my_account.click()
            time.sleep(0.2)
            log_in_name = driver.find_element(By.NAME, "username")
            username = "Thomasss"
            for i in username:
                log_in_name.send_keys(i)
                time.sleep(0.2)
            log_in_password = driver.find_element(By.NAME, "password")
            password = "123456"
            for i in password:
                log_in_password.send_keys(i)
                time.sleep(0.2)
            driver.find_element(By.NAME, "login").click()
            time.sleep(2)

        with allure.step("Наполнение корзины"):
            driver.find_element(
                By.XPATH, '//nav/div/ul/li/a[contains(text(), "Меню")]'
            ).click()
            time.sleep(2)
            driver.find_element(
                By.XPATH, '(//div/div/a[contains(text(), "В корзину")])[1]'
            ).click()
            time.sleep(1)
            driver.find_element(
                By.XPATH, '(//div/div/a[contains(text(), "В корзину")])[10]'
            ).click()
            time.sleep(1)
            driver.find_element(
                By.XPATH, '(//div/div/a[contains(text(), "В корзину")])[4]'
            ).click()
            time.sleep(1)
            driver.find_element(By.CLASS_NAME, "cart-contents").click()
            time.sleep(2)

        with allure.step("Применение купона"):
            coupon_field = driver.find_element(By.NAME, "coupon_code")
            coupon_code = "GIVEMEHALYAVA"
            for i in coupon_code:
                coupon_field.send_keys(i)
                time.sleep(0.2)
            driver.find_element(By.NAME, "apply_coupon").click()
            time.sleep(5)

        with allure.step("Проверка итоговой суммы заказа с учетом скидки"):
            total_price = driver.find_element(By.XPATH, "(//bdi)[8]")
            total_price_text = total_price.text
            assert (
                total_price_text == "873,00₽"
            ), f"Ожидаемая сумма: 873,00 руб, но получено: {total_price_text}"
            allure.attach(
                f"Общая сумма корзины равна {total_price_text}",
                name="Итоговая сумма с учетом скидки",
                attachment_type=allure.attachment_type.TEXT,
            )

    @allure.story("Проверка обработки невалидного купона")
    @allure.description(
        """
    Этот тест выполняет следующие действия:
    1. Открывает главную страницу сайта Pizzeria.
    2. Авторизует пользователя.
    3. Добавляет товары в корзину.
    4. Пытается применить невалидный купон.
    5. Проверяет сообщение об ошибке при применении невалидного купона.
    """
    )
    def test_case_8(self, set_up_browser):
        driver = set_up_browser

        with allure.step("Открытие главной страницы сайта"):
            driver.get("https://pizzeria.skillbox.cc/")
            time.sleep(0.2)

        with allure.step("Авторизация пользователя"):
            my_account = driver.find_element(
                By.XPATH, '//nav/div/ul/li/a[contains(text(), "Мой аккаунт")]'
            )
            my_account.click()
            time.sleep(0.2)
            log_in_name = driver.find_element(By.NAME, "username")
            username = "Thomasss"
            for i in username:
                log_in_name.send_keys(i)
                time.sleep(0.2)
            log_in_password = driver.find_element(By.NAME, "password")
            password = "123456"
            for i in password:
                log_in_password.send_keys(i)
                time.sleep(0.2)
            driver.find_element(By.NAME, "login").click()
            time.sleep(2)

        with allure.step("Наполнение корзины"):
            driver.find_element(
                By.XPATH, '//nav/div/ul/li/a[contains(text(), "Меню")]'
            ).click()
            time.sleep(2)
            driver.find_element(
                By.XPATH, '(//div/div/a[contains(text(), "В корзину")])[1]'
            ).click()
            time.sleep(1)
            driver.find_element(
                By.XPATH, '(//div/div/a[contains(text(), "В корзину")])[10]'
            ).click()
            time.sleep(1)
            driver.find_element(
                By.XPATH, '(//div/div/a[contains(text(), "В корзину")])[4]'
            ).click()
            time.sleep(1)
            driver.find_element(By.CLASS_NAME, "cart-contents").click()
            time.sleep(2)

        with allure.step("Попытка применения невалидного купона"):
            coupon_field = driver.find_element(By.NAME, "coupon_code")
            coupon_code = "DC120"
            for i in coupon_code:
                coupon_field.send_keys(i)
                time.sleep(0.2)
            driver.find_element(By.NAME, "apply_coupon").click()
            time.sleep(2)

        with allure.step("Проверка сообщения об ошибке"):
            alert_message = driver.find_element(By.XPATH, "//div/div/ul/li")
            alert_text = alert_message.text
            assert alert_text == "Неверный купон.", "Применен невалидный купон"
            allure.attach(
                "Невалидный купон не применен",
                name="Результат проверки",
                attachment_type=allure.attachment_type.TEXT,
            )

    @allure.story("Проверка невозможности повторного применения купона")
    @allure.description(
        """
    Этот тест выполняет следующие действия:
    1. Открывает главную страницу сайта Pizzeria.
    2. Авторизует пользователя.
    3. Добавляет товары в корзину.
    4. Применяет купон к заказу.
    5. Пытается применить тот же купон повторно.
    6. Проверяет сообщение о невозможности повторного применения купона.
    """
    )
    def test_case_10(self, set_up_browser):
        driver = set_up_browser

        with allure.step("Открытие главной страницы сайта"):
            driver.get("https://pizzeria.skillbox.cc/")
            time.sleep(0.2)

        with allure.step("Авторизация пользователя"):
            my_account = driver.find_element(
                By.XPATH, '//nav/div/ul/li/a[contains(text(), "Мой аккаунт")]'
            )
            my_account.click()
            time.sleep(0.2)
            log_in_name = driver.find_element(By.NAME, "username")
            username = "Thomasss"
            for i in username:
                log_in_name.send_keys(i)
                time.sleep(0.2)
            log_in_password = driver.find_element(By.NAME, "password")
            password = "123456"
            for i in password:
                log_in_password.send_keys(i)
                time.sleep(0.2)
            driver.find_element(By.NAME, "login").click()
            time.sleep(2)

        with allure.step("Наполнение корзины"):
            driver.find_element(
                By.XPATH, '//nav/div/ul/li/a[contains(text(), "Меню")]'
            ).click()
            time.sleep(2)
            driver.find_element(
                By.XPATH, '(//div/div/a[contains(text(), "В корзину")])[1]'
            ).click()
            time.sleep(1)
            driver.find_element(
                By.XPATH, '(//div/div/a[contains(text(), "В корзину")])[10]'
            ).click()
            time.sleep(1)
            driver.find_element(
                By.XPATH, '(//div/div/a[contains(text(), "В корзину")])[4]'
            ).click()
            time.sleep(1)
            driver.find_element(By.CLASS_NAME, "cart-contents").click()
            time.sleep(2)

        with allure.step("Применение купона"):
            coupon_field = driver.find_element(By.NAME, "coupon_code")
            coupon_code = "GIVEMEHALYAVA"
            for i in coupon_code:
                coupon_field.send_keys(i)
                time.sleep(0.2)
            driver.find_element(By.NAME, "apply_coupon").click()
            time.sleep(5)

        with allure.step(
            "Проверка сообщения о невозможности повторного применения купона"
        ):
            alert_message = driver.find_element(By.XPATH, "//div/div/ul/li")
            alert_text = alert_message.text
            assert (
                alert_text == "Coupon code already applied!"
            ), "Купон применен повторно"
            allure.attach(
                "Купон уже был применен",
                name="Результат проверки",
                attachment_type=allure.attachment_type.TEXT,
            )

    @allure.story("Регистрация в бонусной программе")
    @allure.description(
        """
    Этот тест выполняет следующие действия:
    1. Открывает главную страницу сайта Pizzeria.
    2. Переходит на страницу бонусной программы.
    3. Заполняет форму регистрации в бонусной программе.
    4. Отправляет заявку на регистрацию.
    5. Проверяет появление и содержание всплывающего окна.
    6. Проверяет успешность регистрации в бонусной программе.
    """
    )
    def test_case_11(self, set_up_browser):
        driver = set_up_browser

        with allure.step("Открытие главной страницы сайта"):
            driver.get("https://pizzeria.skillbox.cc/")
            time.sleep(2)

        with allure.step("Переход на страницу бонусной программы"):
            driver.find_element(
                By.XPATH, '//nav/div/ul/li/a[contains(text(), "Бонусная программа")]'
            ).click()
            time.sleep(2)

        with allure.step("Заполнение формы регистрации в бонусной программе"):
            bonus_username = driver.find_element(By.ID, "bonus_username")
            username = "Thomas"
            for i in username:
                bonus_username.send_keys(i)
                time.sleep(0.2)

            bonus_phone = driver.find_element(By.ID, "bonus_phone")
            phone_text = "+72345678901"
            for i in phone_text:
                bonus_phone.send_keys(i)
                time.sleep(0.2)

        with allure.step("Отправка заявки на регистрацию"):
            driver.find_element(By.NAME, "bonus").click()

        with allure.step("Проверка появления и содержания всплывающего окна"):
            try:
                WebDriverWait(driver, 10).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert_text = alert.text
                assert (
                    alert_text
                    == "Заявка отправлена, дождитесь, пожалуйста, оформления карты!"
                ), "Unexpected alert message"
                alert.accept()
                allure.attach(
                    alert_text,
                    name="Текст всплывающего окна",
                    attachment_type=allure.attachment_type.TEXT,
                )
            except TimeoutException:
                allure.attach(
                    "No alert appeared",
                    name="Ошибка",
                    attachment_type=allure.attachment_type.TEXT,
                )

        with allure.step("Проверка успешности регистрации в бонусной программе"):
            success_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h3"))
            )
            success_text = success_message.text
            assert (
                success_text == "Ваша карта оформлена!"
            ), "Регистрация в бонусной программе не прошла!"
            allure.attach(
                "Регистрация в бонусной программе прошла успешно",
                name="Результат проверки",
                attachment_type=allure.attachment_type.TEXT,
            )

    @allure.story("Валидация полей формы бонусной программы")
    @allure.description(
        """
    Этот тест выполняет следующие действия:
    1. Открывает главную страницу сайта Pizzeria.
    2. Переходит на страницу бонусной программы.
    3. Проверяет отправку формы с пустыми полями.
    4. Проверяет ввод некорректного формата телефона.
    5. Проверяет ввод корректных данных и успешную регистрацию.
    """
    )
    def test_case_12(self, set_up_browser):
        driver = set_up_browser

        with allure.step("Открытие главной страницы сайта"):
            driver.get("https://pizzeria.skillbox.cc/")
            time.sleep(2)

        with allure.step("Переход на страницу бонусной программы"):
            driver.find_element(
                By.XPATH, '//nav/div/ul/li/a[contains(text(), "Бонусная программа")]'
            ).click()
            time.sleep(2)

        with allure.step("Проверка отправки формы с пустыми полями"):
            driver.find_element(By.NAME, "bonus").click()
            time.sleep(2)
            error_messages = driver.find_element(By.XPATH, '//*[@id="bonus_content"]')
            error_text = error_messages.text
            assert (
                error_text
                == 'Поле "Имя" обязательно для заполнения\nПоле "Телефон" обязательно для заполнения'
            ), "Ошибки отправки формы с пустыми полями не возникает"
            allure.attach(
                error_text,
                name="Сообщения об ошибках при пустых полях",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Проверка ввода некорректного формата телефона"):
            bonus_username = driver.find_element(By.ID, "bonus_username")
            correct_name = "John Doe"
            for char in correct_name:
                bonus_username.send_keys(char)
                time.sleep(0.2)
            bonus_phone = driver.find_element(By.ID, "bonus_phone")
            incorrect_phone = "123"
            bonus_phone.send_keys(incorrect_phone)
            driver.find_element(By.NAME, "bonus").click()
            time.sleep(2)
            phone_error = driver.find_element(By.ID, "bonus_content")
            assert (
                phone_error.is_displayed()
            ), "Не появляется сообщение об ошибке при вводе некорректного формата телефона"
            allure.attach(
                phone_error.text,
                name="Сообщение об ошибке при некорректном телефоне",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Очистка полей"):
            bonus_phone.clear()
            bonus_username.clear()

        with allure.step("Проверка ввода слишком короткого имени пользователя"):
            bonus_username = driver.find_element(By.ID, "bonus_username")
            incorrect_name = "J"
            bonus_username.send_keys(incorrect_name)
            time.sleep(0.2)
            bonus_phone = driver.find_element(By.ID, "bonus_phone")
            correct_phone = "+79123456789"
            for digit in correct_phone:
                bonus_phone.send_keys(digit)
                time.sleep(0.2)
            driver.find_element(By.NAME, "bonus").click()
            time.sleep(2)
            phone_error = driver.find_element(By.ID, "bonus_content")
            assert (
                phone_error.is_displayed()
            ), "Не появляется сообщение об ошибке при вводе слишком короткого имени пользователя"
            allure.attach(
                phone_error.text,
                name="Сообщение об ошибке при имени пользователя",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Ввод корректных данных и проверка успешной регистрации"):
            correct_name = "John Doe"
            correct_phone = "+79123456789"

            for char in correct_name:
                bonus_username.send_keys(char)
                time.sleep(0.2)

            for digit in correct_phone:
                bonus_phone.send_keys(digit)
                time.sleep(0.2)

            driver.find_element(By.NAME, "bonus").click()

            try:
                WebDriverWait(driver, 10).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert_text = alert.text
                assert (
                    alert_text
                    == "Заявка отправлена, дождитесь, пожалуйста, оформления карты!"
                ), ("Unexpected alert " "message")
                alert.accept()
                allure.attach(
                    alert_text,
                    name="Текст всплывающего окна",
                    attachment_type=allure.attachment_type.TEXT,
                )
            except TimeoutException:
                allure.attach(
                    "No alert appeared after form submission",
                    name="Ошибка",
                    attachment_type=allure.attachment_type.TEXT,
                )
                assert False, "No alert appeared after form submission"

            success_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h3"))
            )
            success_text = success_message.text
            assert (
                success_text == "Ваша карта оформлена!"
            ), "Registration in the bonus program failed"
            allure.attach(
                "Validation of bonus program form fields passed successfully",
                name="Результат проверки",
                attachment_type=allure.attachment_type.TEXT,
            )
