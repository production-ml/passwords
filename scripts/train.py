from lstm_model.base_model import PasswordLSTM


def main():
    password_model = PasswordLSTM()
    password_model.fit(
        train_file="train.csv.zip", test_file="Xtest.csv.zip", epochs=1, batch_size=512
    )
    password_model.save_tokenizer("tokenizer.pickle")
    password_model.save_model("one_epoch_model")


if __name__ == "__main__":
    main()
