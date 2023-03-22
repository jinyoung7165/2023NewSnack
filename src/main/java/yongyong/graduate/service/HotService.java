package yongyong.graduate.service;

import lombok.RequiredArgsConstructor;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;
import yongyong.graduate.common.util.TodayUtil;
import yongyong.graduate.domain.Hot;

import java.util.List;

@Service
@RequiredArgsConstructor
public class HotService {

    private final MongoTemplate mongoTemplate;

    public List<Hot> findAllHot() {
        Query query = new Query();
        query.fields().exclude("_id", "doc");
        List<Hot> hotWords = mongoTemplate.find(query, Hot.class, TodayUtil.todayHot());
        return hotWords;
    }

    public Hot findWordHot(String word) {
        Query hotQuery = new Query();
        hotQuery.fields().include("doc", "weight");
        hotQuery.addCriteria(Criteria.where("word").is(word)).limit(1);
        List<Hot> hots = mongoTemplate.find(hotQuery, Hot.class, TodayUtil.todayHot());
        return hots.get(0);
    }

}
