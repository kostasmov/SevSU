package application;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Stage;

// Точка входа в JavaFX-приложение
public class Main extends Application
{
	// Загрузка JavaFX-приложения
	public static void main(String[] args) { launch(args); }
	
	// Создание и отображение сцены приложения
	@Override public void start(Stage stage) throws Exception
	{
		stage.setTitle("Лабораторная работа №5");
		//stage.setResizable(false);
		stage.setScene(new Scene(FXMLLoader.load(getClass().getResource("Layout.fxml"))));
		stage.show();
	}
}