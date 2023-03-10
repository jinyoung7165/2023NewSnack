package yongyong.graduate.common;

import org.springframework.core.annotation.AliasFor;
import org.springframework.data.mongodb.core.mapping.Document;

import java.lang.annotation.*;

@Today
@Document
@Inherited
@Documented
@Target({ ElementType.TYPE })
@Retention(RetentionPolicy.RUNTIME)
public @interface TodayHot {

    String collection = Today.lastUpdated + "_hot";

    @AliasFor("collection")
    String value() default collection;

    @AliasFor("value")
    String collection() default collection;
}
