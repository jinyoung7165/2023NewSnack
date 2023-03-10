package yongyong.graduate.common.util;

import org.springframework.stereotype.Component;
import yongyong.graduate.common.annotation.TodayDoc;
import yongyong.graduate.common.annotation.TodayHot;

import java.lang.annotation.Annotation;
import java.lang.reflect.Field;
import java.lang.reflect.Proxy;
import java.util.Map;

@Component
public class ReflectUtil { //(collection 이름) 날짜 update 수행

    public static void changeAnnotationValue(String key, Object newValue, Annotation... annotations){
        for (Annotation annotation : annotations) {
            Object handler = Proxy.getInvocationHandler(annotation);
            Field f;
            try {
                f = handler.getClass().getDeclaredField("memberValues");
            } catch (NoSuchFieldException | SecurityException e) {
                throw new IllegalStateException(e);
            }
            f.setAccessible(true);
            Map<String, Object> memberValues;
            if (annotation.annotationType().equals(TodayHot.class)) {
                newValue = newValue + "_hot";
            } else if (annotation.annotationType().equals(TodayDoc.class)) {
                newValue = newValue + "_doc";
            }
            try {
                memberValues = (Map<String, Object>) f.get(handler);
            } catch (IllegalArgumentException | IllegalAccessException e) {
                throw new IllegalStateException(e);
            }
            Object oldValue = memberValues.get(key);
            if (oldValue == null || oldValue.getClass() != newValue.getClass()) {
                throw new IllegalArgumentException();
            }
            memberValues.put(key, newValue);
        }
    }
}
