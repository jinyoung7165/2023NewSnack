package yongyong.graduate.common.annotation;

import org.springframework.core.annotation.AliasFor;
import org.springframework.data.mongodb.core.mapping.Document;
import java.lang.annotation.*;

@Document
@Inherited
@Documented
@Target({ ElementType.TYPE })
@Retention(RetentionPolicy.RUNTIME)
public @interface TodayHot {
    String collection = "2023-03-09_hot";

    @AliasFor("collection")
    String value() default collection;

    @AliasFor("value")
    String collection() default collection;
}
