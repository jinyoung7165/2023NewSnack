package yongyong.graduate;

import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import yongyong.graduate.common.annotation.Today;
import yongyong.graduate.common.util.TodayUtil;
import yongyong.graduate.common.annotation.TodayDoc;
import yongyong.graduate.common.annotation.TodayHot;
import yongyong.graduate.docDomain.Doc;
import yongyong.graduate.hotDomain.Hot;

import javax.annotation.PostConstruct;
import java.time.LocalDate;
import java.util.*;

import static yongyong.graduate.common.util.ReflectUtil.changeAnnotationValue;

@Slf4j
//@SuppressWarnings("unused")
@SpringBootApplication
public class GraduateApplication {
	@PostConstruct
	public void started() {
		TimeZone.setDefault(TimeZone.getTimeZone("Asia/Seoul"));
	}

	
	public static void main(String[] args) {
		Today todayAnt = TodayUtil.class.getAnnotation(Today.class);
		TodayHot todayHotAnt = Hot.class.getAnnotation(TodayHot.class);
		TodayDoc todayDocAnt = Doc.class.getAnnotation(TodayDoc.class);
		changeAnnotationValue("value", LocalDate.now().toString(),
				todayAnt, todayHotAnt, todayDocAnt);
		log.info("updatedToday : {}", TodayUtil.getToday());
		SpringApplication.run(GraduateApplication.class, args);
	}
}

