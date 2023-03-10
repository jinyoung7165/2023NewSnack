package yongyong.graduate;

import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import yongyong.graduate.common.TestClass;
import yongyong.graduate.common.Today;

import javax.annotation.PostConstruct;
import java.lang.annotation.*;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.time.LocalDate;
import java.util.*;

@Slf4j
//@SuppressWarnings("unused")
@SpringBootApplication
public class GraduateApplication {
	@PostConstruct
	public void started() {
		TimeZone.setDefault(TimeZone.getTimeZone("Asia/Seoul"));
	}

	public static void main(String[] args) throws NoSuchMethodException, InvocationTargetException, IllegalAccessException, NoSuchFieldException {
		Today todayAnt = TestClass.class.getAnnotation(Today.class);
		log.info("old today : {}", todayAnt.value());
		Annotation updatedToday = new Today() {
			@Override
			public String value() {
				return LocalDate.now().toString();
			}

			@Override
			public Class<? extends Annotation> annotationType() {
				return todayAnt.annotationType();
			}
		};

		Method method = Class.class.getDeclaredMethod("annotationData", null);
		method.setAccessible(true);
		Object annotationData = method.invoke(TestClass.class, null);
		Field declaredAnnotations = annotationData.getClass().getDeclaredField("declaredAnnotations");
		declaredAnnotations.setAccessible(true);
		Map<Class<? extends Annotation>, Annotation> annotations = (Map<Class<? extends Annotation>, Annotation>) declaredAnnotations.get(annotationData);
		annotations.put(Today.class, updatedToday);
		Today modifiedAnnotation =  TestClass.class.getAnnotation(Today.class);
		log.info("new today : {}", modifiedAnnotation.value());
		SpringApplication.run(GraduateApplication.class, args);
	}
}

